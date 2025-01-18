from awpy import Demo

class Loader:

    def __init__(self):
        pass

    def load_files(self, file_path):
        """
        Maps set of python worker processes onto the list of CS2 file's sent and returns a list of Demo objects each repressenting a parsed game
        """
        parsed_data = self._parse_single_file(file_path)

        return parsed_data

    def _parse_single_file(self, file_path):
        try:
            data = Demo(file_path)
            return data
        except Exception as e:
            print(f"{file_path} has exception {e}")