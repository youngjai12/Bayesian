
from sklearn.cluster import DBSCAN
import numpy as np


def get_embedding_vector():
    file_path = "./data/100000_105000.npz"
    with np.load(file_path, allow_pickle=True) as d:
        urls = d["url"]
        embed = d["embed"]
    return urls, embed



def clusterize(eps, min_sample_cnt):

    urls, embeds = get_embedding_vector()
    cos_sim_dbscan = DBSCAN(eps=eps, min_samples=min_sample_cnt, metric="cosine", n_jobs=5).fit(embeds)
    return cos_sim_dbscan


if __name__ == "__main__":
    dd = clusterize(0.45, 4)
