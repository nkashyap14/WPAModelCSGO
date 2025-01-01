from awpy import Demo
from multiprocessing import Pool
import os

class Loader:

    def __init__(self, num_processes=4):
        self.num_processes = num_processes

    def load_files(self, file_paths):
        """
        Maps set of python worker processes onto the list of CS2 file's sent and returns a list of dictionnary objects each repressenting a parsed game
        """
        with Pool(self.num_processes) as pool:
            parsed_data = pool.map(self._parse_single_file, file_paths)

        return parsed_data

    def _parse_single_file(self, file_path):
        try:
            data = Demo(file_path)
            return data
        except Exception as e:
            print(f"{file_path} has exception {e}")