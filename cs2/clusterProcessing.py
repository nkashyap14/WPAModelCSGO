from src.cluster_processor import ClusterProcessor
import os
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':

    test_path = './cluster_data/mirage/'

    files, files_data = [], {}

    for file in os.listdir(test_path):
        files.append(os.path.join(test_path, file))

    print(files)

    for file in files:
        print(f'computing clusters for file {file}')
        processor = ClusterProcessor(file, min_samples=300)
        base_name = os.path.basename(file)
        output_file = os.path.join(test_path, f'{base_name}_clusters.json')
        clusters = processor.getClusters()
        with open(output_file, 'w') as f:
            json.dump(clusters, f, cls=NumpyEncoder, indent=2)
