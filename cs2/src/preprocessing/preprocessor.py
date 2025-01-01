from .loader import Loader


class Preprocessor:

    def __init__(self, config: dict):
        self.loader = Loader()

    def process_files(self, file_paths: list[str], output='preprocessed_features.csv')
        """
        Takes a list of .dem file paths, parses them utilizing awpy demo parser, loads and engineers feature data necessary for win probability xgboost models and saves them to disk

        Returns:
            bool: True if files are successfully processed and saved, False if anything else occurs
        """

        parsed_data = self.loader.load_files(file_paths)
        