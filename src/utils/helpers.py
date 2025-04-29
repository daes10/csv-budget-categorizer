# system imports
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
        with open(file_path, 'w') as f:
            json.dump(file_data, f, indent=4)

    @staticmethod
    def update_json_file(file_path: str, new_data: dict) -> dict:
        """Update JSON file with new data without losing existing content"""
        # Read existing data
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        
        # Update existing data with new data
        existing_data.update(new_data)
        
        # Write combined data back to file
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
        
        return existing_data