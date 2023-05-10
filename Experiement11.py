import numpy as np
from scipy.spatial.distance import cdist
from scipy import cluster
from sklearn.cluster import KMeans
import pandas as pd

# Proclus combines both hierarchical and k-means clustering

class Proclus:
    # ward linkage function specifies the distance between two clusters as the increase in
    # the "error sum of squares" after fusing two clusters into a single cluster
    def __init__(self, n_clusters, k_subset, linkage='ward'):
        self.n_clusters = n_clusters
        self.k_subset = k_subset
        self.linkage = linkage
        
    def fit(self, X):
        # Phase 1: hierarchical clustering
        # euclidean distance of each point from each other point
        dist_matrix = cdist(X, X, metric='euclidean')
        # create hierarchical clustering using ward linkage
        hierarchy = cluster.hierarchy.ward(dist_matrix)
        # given a linkage matrix, it returns a cut_tree. 
        # cut_tree is an array indicating group membership at each agglometration step
        cutree = cluster.hierarchy.cut_tree(hierarchy, n_clusters=self.n_clusters).flatten()
        

        # Phase 2: k-means clustering on each cluster
        clusters = {}
        for i in range(self.n_clusters):
            indices = np.where(cutree == i)[0]
            if len(indices) < self.k_subset:
                continue
            cluster_X = X[indices]
            kmeans = KMeans(n_clusters=self.k_subset).fit(cluster_X)
            clusters[i] = kmeans.cluster_centers_
        
        # Merge clusters based on Jaccard similarity
        self.labels_ = np.zeros(len(X))
        for i in range(self.n_clusters):
            for j in range(i + 1, self.n_clusters):
                if i not in clusters or j not in clusters:
                    continue
                i_indices = np.where(cutree == i)[0]
                j_indices = np.where(cutree == j)[0]
                i_kmeans = KMeans(n_clusters=self.k_subset, init=clusters[i]).fit(X[i_indices])
                j_kmeans = KMeans(n_clusters=self.k_subset, init=clusters[j]).fit(X[j_indices])
                i_labels = i_kmeans.labels_
                j_labels = j_kmeans.labels_
                jaccard_sim = len(set(i_labels).intersection(j_labels)) / len(set(i_labels).union(j_labels))
                if jaccard_sim > 0.5:
                    self.labels_[i_indices] = i
                    self.labels_[j_indices] = j
        unassigned_indices = np.where(self.labels_ == 0)[0]
        if len(unassigned_indices) > 0:
            kmeans = KMeans(n_clusters=self.n_clusters).fit(X[unassigned_indices])
            self.labels_[unassigned_indices] = kmeans.labels_ + self.n_clusters
        
        return self
    


data = pd.read_csv("/Users/palak/Documents/BTech/8th_Sem/BDA/Experiments/BankChurners.csv")
print(data.head())

obj_columns = []
for i in data.columns:
    if data[i].dtype == object:
        obj_columns.append(i)

one_hot_encoded_data = pd.get_dummies(data, columns=obj_columns)
print(one_hot_encoded_data.head())
proclus = Proclus(n_clusters=3, k_subset=3)

proclus.fit(one_hot_encoded_data)
labels = proclus.labels_
print("labels: ", labels)