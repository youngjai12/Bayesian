
# DB Scan 
똑같은 input-data에 대해서 아래와 같이 하면 memory가 일단 터진다.(dist-matrix구할때)
- metric="pre-computed"
- fit()에 dist-matrix 준다. 

그런데 라이브러리상에서는 같은 데이터 넣어줘도, dist-matrix 구하다가 memeory 안터지고 잘 나온다....

## 왜 라이브러리는 메모리 안터지나? 
=> key idea : dist-matrix를 chunk로 나눠서 구하더라...  
### `pairwise_distances_chunked`
`pairwise.py` 에 있음.     
Generate a distance matrix chunk by chunk with optional reduction.
``` 
In cases where not all of a pairwise distance matrix needs to be
stored at once, this is used to calculate pairwise distances in
``working_memory``-sized chunks.  If ``reduce_func`` is given, it is
run on each chunk and its return values are concatenated into lists,
arrays or sparse matrices.
```
#### 역할설명 
- 모든 distance가 한번에 계산될 필요가 없을 경우에는, 그래서 한번에 저장되어야할 필요가 없을때
-  working-memory-size 만큼씩으로 chunk를 나눠서 계산한다. 
- 이렇게 나눠진 chunk 에는 reduce_func를 적용한다. 
- chunk가 return 된다. (D_chunk : {ndarray, sparse matrix})

#### 내부 원리 
- 아래와 같은 함수를 통해서 chunk 가 return 된다.
```python
chunk_n_rows = get_chunk_n_rows(
            row_bytes=8 * _num_samples(Y),
    max_n_rows=n_samples_X,
    working_memory=working_memory,
)
slices = gen_batches(n_samples_X, chunk_n_rows)
```

### `reduce_func`

- 역할 
```
reduce_func(D_chunk, start)
is called repeatedly, where ``D_chunk`` is a contiguous vertical
slice of the pairwise distance matrix, starting at row ``start``.
It should return one of: None; an array, a list, or a sparse matrix
of length ``D_chunk.shape[0]``; or a tuple of such objects.
Returning None is useful for in-place operations, rather than
reductions.

If None, pairwise_distances_chunked returns a generator of vertical
chunks of the distance matrix.
```
아래와 같이 사용된다. 

```python
reduce_func = partial(
                self._radius_neighbors_reduce_func,
                radius=radius,
                return_distance=return_distance,
            )
```
