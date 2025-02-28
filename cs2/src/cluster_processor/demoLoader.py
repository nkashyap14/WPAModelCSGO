from awpy import Demo
import psutil
import pandas as pd
import os

class ClusterDemoLoader:
    """
    Class that parses a singel demo and extracts feature set related to calculating DBSCan centroids.
    At the end cleans up all data related to parsing a demo. Meant to be cleaned up as well. Used to encapsulate
    creeping memory usage in programs that parse multiple demos at a time.
    """
    def __init__(self, output_folder="./cluster_data", invalid_folder="D:\\CS_2_DEMOS"):
        self.output_dir = output_folder
        self.invalid_dir = os.path.join(invalid_folder, "invalid_demos")
        os.makedirs(self.invalid_dir, exist_ok=True)



    def extractClusterStatistics(self, demo_path, map_name):
        print(f"Memory usage at the beginning of extracting cluster statistics: {self._get_memory_usage():.2f} MB")
        try:
            data = self._parse_single_file(demo_path)
            ct_data, t_data = self._extractClusterStatistics(data)

            output_dir = os.path.join(self.output_dir, map_name)

            output_path_ct = os.path.join(output_dir, 'ct_data.csv')
            output_path_t = os.path.join(output_dir, 't_data.csv')

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            ct_data.to_csv(output_path_ct, mode='a', header = not os.path.exists(output_path_ct), index=False)
            t_data.to_csv(output_path_t, mode='a', header = not os.path.exists(output_path_t), index=False)

            del data, ct_data, t_data
            print(f"Memory usage after extraction and saving extracted data points: {self._get_memory_usage():.2f} MB")
        except Exception as e:
            print(e)
            print(f"Memory usage after failing to extract due to exception is: {self._get_memory_usage():.2f} MB")


    def _get_memory_usage(self):
        process = psutil.Process()
        #RSS refers to Resident Set Size which is the portion of the process's memory that is currently held in 
        #physical memory
        return process.memory_info().rss / 1024 / 1024 #conversion to MB


    def _extractClusterStatistics(self, data):

        print(f"Memory usage before parsing demo: {self._get_memory_usage():.2f} MB")

        kills_df = data.kills

        ct_kills = kills_df[kills_df['attacker_team_name'] == 'CT']
        ct_data = pd.DataFrame({
            'X': ct_kills['attacker_X'],
            'Y': ct_kills['attacker_Y'],
            'Z': ct_kills['attacker_Z'],
            'weapon': ct_kills['weapon']
        })

        t_kills = kills_df[kills_df['attacker_team_name'] == 'TERRORIST']
        t_data = pd.DataFrame({
            'X': t_kills['attacker_X'],
            'Y': t_kills['attacker_Y'],
            'Z': t_kills['attacker_Z'],
            'weapon': t_kills['weapon']
        })

        print(f"Memory usage after extracting ct + t kills {self._get_memory_usage():.2f} MB")

        del t_kills, ct_kills, kills_df

        print(f"Memory usage after cleaning up dataframes in _extractClusterStatistics {self._get_memory_usage():.2f} MB")

        return (ct_data, t_data)

        
    def _parse_single_file(self, demo_path):
        try:
            data = Demo(demo_path)
            return data
        except Exception as e:
            print(f"{demo_path} has exception {e}")
            if "Source1DemoError" in str(e):
                try:
                    # Get just the filename
                    file_name = os.path.basename(demo_path)
                    # Create new path in invalid_demos directory
                    new_path = os.path.join(self.invalid_dir, file_name)
                    print(f"Moving {demo_path} to {new_path} as it is a Source1 demo")
                    # Move the file instead of deleting it
                    import shutil
                    shutil.move(demo_path, new_path)
                except (PermissionError, OSError) as move_error:
                    print(f"Unable to move file due to permissions: {move_error}")
                    # Create a log of invalid files instead
                    with open(os.path.join(self.output_dir, "invalid_demos.txt"), "a") as f:
                        f.write(f"{demo_path}\n")