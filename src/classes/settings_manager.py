# system imports
import os
import json
import tkinter as tk
from tkinter import ttk

# local imports
from ..utils import Helper

class SettingsManager:
    """Handles loading, saving, and managing settings."""    
    def __init__(self, app, settings_path) -> None:
        self.app = app  # Store the App instance
        self.settings_path = settings_path
        self.settings_data = {}

        # Ensure the settings are loaded at the beginning
        self.load_settings()
    
    def __str__(self) -> str:
        """Returns a string representation of the SettingsManager instance."""
        return f"SettingsManager: \n  -> settings_path= {self.settings_path},\n  -> settings_data= {self.settings_data}"

    def create_settings_file(self) -> None:
        """Creates the settings file if it doesn't exist."""
        if not os.path.exists(self.settings_path):
            Helper.create_dir(self.settings_path)
            self.settings_data = {
                # "paths": {
                #     "input_path": "",
                #     "output_path": ""
                # },
                "preset_menu": {
                    "presets": [],
                    "selected_preset": ""
                }
            }
            Helper.save_file(self.settings_path, self.settings_data)
        else:
            print(f"The following path is already existing!\n => {self.settings_path}")

    def load_settings(self) -> None:
        """Loads settings from the JSON file."""
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                self.settings_data = json.load(f)
        else:
            self.create_settings_file()


