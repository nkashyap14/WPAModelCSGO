from .extractor import Extractor
from .loader import Loader
from .transformer import Transformer
import time
import json
import numpy as np

def convert_to_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    return obj

class Preprocessor:

    def __init__(self, config: dict):
        self.loader = Loader(config['loader'])
        self.transformer = Transformer(config['transformer'])
        self.extractor = Extractor(config['extractor'])


    def process_files(self, file_paths: list[str], feature_output='preprocessed_features.csv'):
        """
        Takes a list of .dem file paths, parses them utilizing awpy demo parser, loads and engineers feature data necessary for win probability xgboost models and saves them to disk

        Returns:
            bool: True if files are successfully processed and saved, False if anything else occurs
        """
        overall_start = time.time()
        print(f"Parsing {len(file_paths)} demos")
        start = time.time()
        parsed_data = self.loader.load_files(file_paths)
        print(f"Parsed demos in {time.time() - start} seconds")
        print(len(parsed_data))
        print('Extracting features')
        start = time.time()
        vectors = self.extractor.extractFeatures(parsed_data)
        print(type(vectors))
        print(f"Exctracted features from {len(file_paths)} in {time.time() - start} seconds")
        print(f"Extracted a total of {len(vectors)} feature vectors")
        print(type(vectors))

        start = time.time()
        transformed_data = self.transformer.transform_data(vectors)
        print(f"Transformed all extracted features in {time.time() - start} seconds. now saving them to disk")

        transformed_data.to_csv(feature_output)

        print(f"Overall process of parsing {len(file_paths)} demos and extracting features and transformign them took  {time.time() - overall_start} seconds")
'''
        output = {}
        for match_id, vector in vectors.items():
            output[match_id] = [convert_to_serializable(v) for v in vector]
            break

        with open('feature_vectors.json', 'w') as fp:
            json.dump(output, fp)

'''