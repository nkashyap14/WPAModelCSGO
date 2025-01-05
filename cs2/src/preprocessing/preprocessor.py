from .loader import Loader
from .extractor import Extractor
from .transformer import Transformer
from multiprocessing import Pool
import os


class Preprocessor:

    def __init__(self):
        self.loader = Loader()
        self.extractor = Extractor()
        self.transformer = Transformer()

    def process_files(self, file_paths: list[str], output_dir='./features/', num_processes=4):
        """
        Takes a list of .dem file paths, parses them utilizing awpy demo parser, loads and engineers feature data necessary for win probability xgboost models and saves them to disk

        Returns:
            bool: True if files are successfully processed and saved, False if anything else occurs
        """

        with Pool(num_processes) as pool:
            pool.starmap(self._process_file, [(file, f"{output_dir}preprocessed_{os.path.basename(file).split('.')[0]}") for file in file_paths])


    def _process_file(self, file_path, output):
        print(f"{os.getpid()} is starting to parse {os.path.basename(file_path)}")
        parsed_data = self.loader.load_files(file_path)
        print(f"{os.getpid()} has gone past loader. now going into extractor")
        vectors = self.extractor.extractFeatures(parsed_data)
        print(f"{os.getpid()} has gone past extraction now going into transformer")
        transformed_data = self.transformer.fit_transform(vectors)

        transformed_data.to_csv(output, index=False)