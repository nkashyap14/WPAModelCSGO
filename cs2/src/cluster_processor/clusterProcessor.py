from sklearn.cluster import DBSCAN
from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np

class ClusterProcessor:
    def __init__(self, ct_file_path, t_file_path, eps=200, min_samples=5):
        self.ct_file_path = ct_file_path
        self.t_file_path = t_file_path
        self.eps = eps
        self.min_samples = min_samples

    def computeClusters(self):
        self._computeDBSCANModel()
        self._compute_clusters()
        self._compute_kd_ratios()


    def _computeDBSCANModel(self):
        self.ctdata = pd.read_csv(self.ct_file_path)[['X', 'Y', 'Z']]
        self.tdata = pd.read_csv(self.t_file_path)[['X', 'Y', 'Z']]
        self.ctdbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(self.ctdata[['X', 'Y', 'Z']].values)
        self.tdbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(self.tdata[['X', 'Y', 'Z']].values)        

    def _compute_clusters(self):
        #grab cluster labels for each point
        ctlabels = self.ctdbscan.labels_
        tlabels = self.tdbscan.labels_

        self.ctclusters = self._compute_labels(ctlabels, self.ctdata)
        self.tclusters = self._compute_labels(tlabels, self.tdata)

    def _compute_labels(self, labels, data):

        clusters = {}

        for label in set(labels):
            if label == -1:
                continue
            
            mask = labels == label
            points = data[mask]

            clusters[label] = {
                'center_x': points['X'].mean(),
                'center_y': points['Y'].mean(),
                'center_z': points['Z'].mean(),
                'point_count': len(points),
            }

        return clusters

#{
#                'center_x': points['X'].mean(),
#                'center_y': points['Y'].mean(),
#                'center_z': points['Z'].mean(),
#                'point_count': len(points),
#                'points': points[['X', 'Y', 'Z']].values,
#                'weapons': points['weapon'].value_counts().to_dict()
#            }


    def _compute_kd_ratios(self):
        if not len(self.ctdata) or not len(self.tdata):
            return {}
        
        ct_tree = KDTree(self.ctdata)
        t_tree = KDTree(self.tdata)

        self.t_kd_ratios = self._getClusterStats(ct_tree, t_tree, self.tclusters)
        self.ct_kd_ratios = self._getClusterStats(ct_tree, t_tree, self.ctclusters)

    
    def _getClusterStats(self, ct_tree, t_tree, cluster_stats, radius=200):
        kd_ratios = {}
        
        for cluster_id, stats in cluster_stats.items():
            center = np.array([[stats['center_x'], stats['center_y'], stats['center_z']]])
            ct_count = len(ct_tree.query_radius(center, r=radius)[0])
            t_count = len(t_tree.query_radius(center, r=radius)[0])
            
            kd_ratios[cluster_id] = {
                'ct_kills': ct_count,
                't_kills': t_count,
                'ct_kd_ratio': ct_count / max(t_count, 1),
                't_kd_ratio': t_count / max(ct_count, 1),
                'total_kills': ct_count + t_count
            }
        
        return kd_ratios

    def getKDRatios(self):
        return (self.ct_kd_ratios, self.t_kd_ratios)
    
    def getClusters(self):
        return (self.ctclusters, self.tclusters)