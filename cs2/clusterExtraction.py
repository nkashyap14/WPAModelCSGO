#from src.cluster_processor import ClusterProcessor
import os
from src.cluster_processor import ClusterDemoLoader
import psutil

def _get_memory_usage():
    process = psutil.Process()
    #RSS refers to Resident Set Size which is the portion of the process's memory that is currently held in 
    #physical memory
    return process.memory_info().rss / 1024 / 1024 #conversion to MB


if __name__ == '__main__':
    '''
    processor = ClusterProcessor(
        demo_dir="D:\\CS_2_DEMOS\\",
        output_dir="./cluster_data",
        batch_size=10
    )

    # Process all maps
    processor.process_all_maps()
    '''

    dir_path = 'D:\\CS_2_DEMOS'
    maps = ['vertigo']

    files, files_data = [], {}

    for file in os.listdir(dir_path):
        files.append(os.path.join(dir_path, file))

    for map in maps:
        files_data[map] = [file for file in files if map in file]

    loader = ClusterDemoLoader()
    for map in files_data:
        for i, file in enumerate(files_data[map]):
            print(f"Memory usage before extracting file {i} at path {file} for map {map} is {_get_memory_usage():.2f} MB ")
            loader.extractClusterStatistics(file, map)
            print(f"Memory usage after extracting file {i} at path {file} for map {map} is {_get_memory_usage():.2f} MB ")