# Helper Class
import os
import json

class Helper:
    """Helper methods"""
    def __init__(self):
        pass

    @staticmethod
    def create_dir(dir_path: str) -> None:
        """Creates the specified directory if it doesn't exist."""
        if not os.path.exists(dir_path):
            dir_name = os.path.dirname(dir_path)
            os.makedirs(dir_name,exist_ok=True)
        else:
            print("Path is already existing. It can not be created!")
    
    @staticmethod
    def save_file(file_path: str, file_data: dict) -> None:
        """Saves a file."""
        with open(file_path, "w") as f:
            json.dump(file_data, f, indent=4)
