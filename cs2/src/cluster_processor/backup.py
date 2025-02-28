import os
import pickle
import numpy as np
import pandas as pd
from awpy import Demo
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KDTree
from tqdm import tqdm
import gc
import traceback
import time
import psutil

class BatchStatistics:
    def __init__(self, ct_positions, t_positions, batch_number):
        self.batch_number = batch_number
        self.ct_count = len(ct_positions)
        self.t_count = len(t_positions)
        
        ct_dbscan = DBSCAN(eps=200, min_samples=5).fit(ct_positions[['X', 'Y', 'Z']].values)
        t_dbscan = DBSCAN(eps=200, min_samples=5).fit(t_positions[['X', 'Y', 'Z']].values)
        
        self.ct_clusters = self._compute_batch_clusters(ct_positions, ct_dbscan)
        self.t_clusters = self._compute_batch_clusters(t_positions, t_dbscan)
    
    def _compute_batch_clusters(self, positions_df, dbscan_model):
        clusters = []
        labels = dbscan_model.labels_
        
        for label in set(labels):
            if label == -1:
                continue
                
            mask = labels == label
            points = positions_df[mask]
            
            clusters.append({
                'center_x': points['X'].mean(),
                'center_y': points['Y'].mean(),
                'center_z': points['Z'].mean(),
                'point_count': len(points),
                'points': points[['X', 'Y', 'Z']].values,
                'weapons': points['weapon'].value_counts().to_dict()
            })
        
        return clusters

class ClusterProcessor:
    def __init__(self, demo_dir, output_dir, batch_size=10):
        self.demo_dir = demo_dir
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.maps = ['anubis', 'ancient', 'dust2', 'vertigo']
        
        self.temp_dir = os.path.join(output_dir, 'temp')
        self.final_dir = os.path.join(output_dir, 'final')
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.final_dir, exist_ok=True)

    def _get_map_files(self):
        files_by_map = {map_name: [] for map_name in self.maps}
        
        for file in os.listdir(self.demo_dir):
            if file.endswith('.dem'):
                for map_name in self.maps:
                    if map_name in file.lower():
                        files_by_map[map_name].append(os.path.join(self.demo_dir, file))
                        break
        
        return files_by_map
    
    def _get_memory_usage(self):
        """Get current memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB


    def process_batch(self, batch_files, map_name, batch_number):
        all_ct_kills = []
        all_t_kills = []
        
        print(f"\nProcessing batch {batch_number} ({len(batch_files)} files)")
        print(f"Initial batch memory usage: {self._get_memory_usage():.2f} MB")
        
        for file in tqdm(batch_files, desc=f"Batch {batch_number}"):
            try:
                print(f"\nParsing: {os.path.basename(file)}")
                print(f"Memory before parsing: {self._get_memory_usage():.2f} MB")
                
                parser = Demo(file, verbose=False)
                print(f"Memory after parser creation: {self._get_memory_usage():.2f} MB")
                
                kills_df = parser.kills
                print(f"Memory after loading kills: {self._get_memory_usage():.2f} MB")
                print(f"Loaded {len(kills_df)} kills")
                
                # Extract CT kills
                ct_kills = kills_df[kills_df['attacker_team_name'] == 'CT']
                ct_data = pd.DataFrame({
                    'X': ct_kills['attacker_X'],
                    'Y': ct_kills['attacker_Y'],
                    'Z': ct_kills['attacker_Z'],
                    'weapon': ct_kills['weapon']
                })
                print(f"Memory after CT extraction: {self._get_memory_usage():.2f} MB")
                
                # Extract T kills
                t_kills = kills_df[kills_df['attacker_team_name'] == 'TERRORIST']
                t_data = pd.DataFrame({
                    'X': t_kills['attacker_X'],
                    'Y': t_kills['attacker_Y'],
                    'Z': t_kills['attacker_Z'],
                    'weapon': t_kills['weapon']
                })
                print(f"Memory after T extraction: {self._get_memory_usage():.2f} MB")
                
                all_ct_kills.append(ct_data)
                all_t_kills.append(t_data)
                
                print(f"Memory before cleanup: {self._get_memory_usage():.2f} MB")
                del parser, kills_df, ct_kills, t_kills
                gc.collect()
                print(f"Memory after cleanup: {self._get_memory_usage():.2f} MB\n")
                
            except Exception as e:
                print(f"Error processing {os.path.basename(file)}: {str(e)}")
                print(f"Memory at error: {self._get_memory_usage():.2f} MB")
                continue
        
        if all_ct_kills and all_t_kills:
            print(f"\nMemory before batch concatenation: {self._get_memory_usage():.2f} MB")
            # Combine kills for this batch
            batch_ct = pd.concat(all_ct_kills, ignore_index=True)
            batch_t = pd.concat(all_t_kills, ignore_index=True)
            print(f"Memory after batch concatenation: {self._get_memory_usage():.2f} MB")
            
            # Calculate batch statistics
            print("Computing batch statistics...")
            batch_stats = BatchStatistics(batch_ct, batch_t, batch_number)
            print(f"Memory after computing statistics: {self._get_memory_usage():.2f} MB")
            
            # Save batch statistics
            stats_file = os.path.join(self.temp_dir, f"{map_name}_batch_{batch_number}_stats.pkl")
            with open(stats_file, 'wb') as f:
                pickle.dump(batch_stats, f)
            print(f"Saved batch {batch_number} statistics")
            
            print(f"\nMemory before final batch cleanup: {self._get_memory_usage():.2f} MB")
            del batch_ct, batch_t, all_ct_kills, all_t_kills, batch_stats
            gc.collect()
            gc.collect()
            print(f"Memory after final batch cleanup: {self._get_memory_usage():.2f} MB")
            time.sleep(2)  # Give more time for memory to settle

    def _compute_final_clusters(self, points_array, min_samples=5):
        dbscan = DBSCAN(eps=200, min_samples=min_samples).fit(points_array)
        
        cluster_stats = {}
        labels = dbscan.labels_
        
        for label in set(labels):
            if label == -1:
                continue
                
            mask = labels == label
            cluster_points = points_array[mask]
            
            cluster_stats[label] = {
                'center_x': np.mean(cluster_points[:, 0]),
                'center_y': np.mean(cluster_points[:, 1]),
                'center_z': np.mean(cluster_points[:, 2]),
                'count': len(cluster_points)
            }
        
        return cluster_stats

    def _compute_kd_ratios(self, ct_points, t_points, cluster_stats, radius=200):
        if len(ct_points) == 0 or len(t_points) == 0:
            return {}
            
        ct_tree = KDTree(ct_points)
        t_tree = KDTree(t_points)
        
        kd_ratios = {}
        
        for cluster_id, stats in cluster_stats.items():
            center = np.array([[stats['center_x'], stats['center_y'], stats['center_z']]])
            ct_count = len(ct_tree.query_radius(center, r=radius)[0])
            t_count = len(t_tree.query_radius(center, r=radius)[0])
            
            kd_ratios[cluster_id] = {
                'ct_kills': ct_count,
                't_kills': t_count,
                'kd_ratio': ct_count / max(t_count, 1),
                'total_kills': ct_count + t_count
            }
        
        return kd_ratios

    def combine_batch_statistics(self, map_name):
        print(f"\nCombining statistics for {map_name}")
        batch_files = [f for f in os.listdir(self.temp_dir) 
                      if f.startswith(f"{map_name}_batch") and f.endswith("_stats.pkl")]
        
        all_ct_points = []
        all_t_points = []
        
        for batch_file in tqdm(batch_files, desc="Loading batches"):
            with open(os.path.join(self.temp_dir, batch_file), 'rb') as f:
                batch_stats = pickle.load(f)
                
                for cluster in batch_stats.ct_clusters:
                    all_ct_points.extend(cluster['points'])
                for cluster in batch_stats.t_clusters:
                    all_t_points.extend(cluster['points'])
        
        all_ct_points = np.array(all_ct_points)
        all_t_points = np.array(all_t_points)
        
        print("Computing final clusters...")
        ct_cluster_stats = self._compute_final_clusters(all_ct_points)
        t_cluster_stats = self._compute_final_clusters(all_t_points)
        
        print("Computing K/D ratios...")
        ct_kd_ratios = self._compute_kd_ratios(all_ct_points, all_t_points, ct_cluster_stats)
        t_kd_ratios = self._compute_kd_ratios(all_ct_points, all_t_points, t_cluster_stats)
        
        final_data = {
            'ct_cluster_stats': ct_cluster_stats,
            't_cluster_stats': t_cluster_stats,
            'ct_kd_ratios': ct_kd_ratios,
            't_kd_ratios': t_kd_ratios
        }
        
        with open(os.path.join(self.final_dir, f"{map_name}_clusters.pkl"), 'wb') as f:
            pickle.dump(final_data, f)
        
        print(f"Saved final clusters for {map_name}")
        
        # Clean up temp files
        for batch_file in batch_files:
            os.remove(os.path.join(self.temp_dir, batch_file))

    def process_map(self, map_name, files):
        print(f"\nProcessing {map_name} ({len(files)} files)")
        
        for i in range(0, len(files), self.batch_size):
            batch_files = files[i:i + self.batch_size]
            self.process_batch(batch_files, map_name, i // self.batch_size)
            time.sleep(1)  # Brief pause between batches
        
        self.combine_batch_statistics(map_name)

    def process_all_maps(self):
        print(f"Initial process memory: {self._get_memory_usage():.2f} MB")
        files_by_map = self._get_map_files()
        
        for map_name, files in files_by_map.items():
            if not files:
                print(f"No files found for {map_name}")
                continue
            
            try:
                print(f"\nStarting {map_name} processing. Memory: {self._get_memory_usage():.2f} MB")
                self.process_map(map_name, files)
                print(f"Completed {map_name}. Memory: {self._get_memory_usage():.2f} MB")
            except Exception as e:
                print(f"Error processing {map_name}:")
                print(traceback.format_exc())
                print(f"Memory at error: {self._get_memory_usage():.2f} MB")
                continue