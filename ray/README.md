# Ray 
. Ray는 분산 애플리케이션을 위한 단순하고 범용적인 API를 제공
### 장점
* multi-processing 은 병렬처리를 위해서 코드를 고쳐써야했음.-> 그럴 필요가 없음
* multi-processing 에서 발생하는 직렬화 오버헤드 문제가 발생하지 않는다. 
  * 직렬화 오버헤드를 해결하기 위해 Apache Arrow를 사용
  *  Apache Arrow는 행(Row) 기반이 아닌 컬럼 기반의 인메모리 포맷으로 Zero-Copy 직렬화를 수행
  *  직렬화된 데이터를 인메모리 객체 저장소 (In-Memory Object Store)인 Plasma를 이용해 직렬화된 데이터를 빠르게 공유
### 목표 
1. single-node ray & multi-node ray 간의 차이     
->   설명을 봤을 때, multi-node ray cluster 는 다르다고 하는걸 보면, single-node ray 와는 다른것 같다.        
->  local에서 돌리는건 single-node인건지? 아니면 cpu가 여러개라서 multi-node인건지...?     
         

* 세팅 환경 
* 성능 비교 
* 모니터링 
2. 모델링 성능 비교


## 설치 
* `pip install ray`
  * 
* `pip install -U "ray[default]`
    * dashboard 랑 cluster 를 띄우기 위해서 필요한 install
* `pip install -U ray`
    * minimal dependency 로 설치하는 것 
  
## ray_init() 설정 
#### memory 설정 
* 방법 
  `ray.init(object_store_memory=4 * 1024 * 1024 * 1024) # 4GB`
  
* 의미 혹은 의의  
  * 
