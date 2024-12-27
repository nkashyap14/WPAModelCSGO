from awpy import DemoParser
from multiprocessing import Pool
import os

class Loader:
    """
    A Data loader class for the win probabilty model being set up by Nikhilesh Kashyap. Will utilize the awpy class alongside with multiprocessing functionality to parse the demos and then return their data objects.
    Takes in a configuration value which represents the number of python processes to initiate while simultaneously parsing. The reason multiprocessing was chosen over multithreading is the parsing work is CPU intensive
    and not I/O intensive which due to the restrictions of the GIL requires us to set up alternative python interpretive processes to leverage parallel execution.
    """
    def __init__(self, config: dict):
        self.num_processes = config.get('num_processes')
        self.parse_rate = config.get('parse_rate')

    def load_files(self, file_paths):
        """
        Maps set of python worker processes onto the list of file's sent and returns the combined version of the parsed data
        """
        with Pool(self.num_processes) as pool:
            parsed_data = pool.map(self._parse_single_file, file_paths)
        return parsed_data
    
    def _parse_single_file(self, file_path):
        """
        Takes in a single .dem file and parses it and returns the output in dataframe format
        """
        file_name = os.path.basename(file_path)
        parser = DemoParser(demofile=file_path, demo_id=file_name, parse_rate=self.parse_rate)
        return parser.parse(return_type="df")