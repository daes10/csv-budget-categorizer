# Settings Manager Class
import tkinter as tk
from tkinter import ttk
import os
import json
from HelperClass import Helper




class SettingsManager:
    """Handles loading, saving, and managing settings."""    
    def __init__(self, settings_path="./data/settings.json") -> None:
        self.settings_path = settings_path
        self.settings_data = {}

        # Ensure the settings are loaded at the beginning
        self.load_settings()



    def create_settings_file(self) -> None:
        """Creates the settings file if it doesn't exist."""
        settings_path = "test"
        if not os.path.exists(self.settings_path):
            Helper.create_dir(self.settings_path)
            Helper.save_file(self.settings_path, self.settings_data)
        else:
            print(f"The following path is already existing!\n => {settings_path}")

    def load_settings(self) -> None:
        """Loads settings from the JSON file."""
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                self.settings_data = json.load(f)
        else:
            self.create_settings_file()

    def get_paths(self, entry_input: ttk.Entry, entry_output: ttk.Entry):
        """Loads all the Settings from a file and sets the filepaths to the corresponding entryfields."""
        self.load_settings()
        entry_input.insert(0, self.settings_data["paths"]["input_path"])
        entry_output.insert(0, self.settings_data["paths"]["output_path"])

    def set_paths(self, input_path: str, output_path: str) -> None:
        """Sets and saves the input and output paths."""
        if os.path.exists(self.settings_path):
            self.settings_data["paths"]["input_path"] = input_path
            self.settings_data["paths"]["output_path"] = output_path
            Helper.save_file(self.settings_path, self.settings_data)
        else:
            # Opens a messagebox to inform the user
            tk.messagebox.showinfo("Info", "No permission to create a settingsfile!")
