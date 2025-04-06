# Settings Manager Class
import tkinter as tk
from tkinter import ttk
import os
import json
from HelperClass import Helper




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


class PresetManager(SettingsManager):
    """Handles loading, saving, and managing presets."""
    def __init__(self, app, settings_path) -> None:
        super().__init__(app, settings_path) # Call the parent constructor and initialize the required properties

        # Validate settings_path
        if not settings_path:
            raise ValueError("settings_path cannot be empty.")

        # Define preset properties
        self.presets = self.settings_data.get("preset_menu", {}).get("presets", [])
        # If no presets are found, create one default preset
        if not self.presets:
            self.presets = ["Default Preset"]  # Default preset

        # Set the default preset if none is found in settings
        self.selected_preset = tk.StringVar(value=self.settings_data.get("preset_menu", {}).get("selected_preset") or self.presets[0])

        # If we're using the default value, save it to ensure it's properly stored
        if not self.settings_data.get("preset_menu", {}).get("selected_preset"):
            self.set_presets()  # Save the default preset
        
        # Preset variables
        self.preset_dir_path  = os.path.dirname(self.settings_path)  # Get the directory path
        self.preset_path = self.get_preset_path()  # Get the full preset path
        self.preset_data = {}

        # Create preset file if it doesn't exist
        self.create_presets_file(self.get_preset_path())

        # Load the current presets
        self.load_presets()


    def __str__(self) -> str:
        """Returns a string representation of the PresetManager instance."""
        return f"PresetManager: \n  -> presets= {self.presets},\n  -> selected_preset= {self.selected_preset.get()},\n  -> settings_path= {self.settings_path},\n  -> settings_data= {self.settings_data}"

    def get_preset_path(self, filename: str= None) -> str:
        """Returns the path to the current selected preset file or a defined one."""
        if filename is None:
            preset_full_path_slashes = os.path.join(self.preset_dir_path, f"{self.get_selected_preset()}.json")
        else:
            preset_full_path_slashes = os.path.join(self.preset_dir_path, filename)
        
        preset_full_path = preset_full_path_slashes.replace("\\", "/") # Replace backslashes with forward slashes
        # * DEBUGGING
        # print(f"Preset path: {preset_full_path}")
        return preset_full_path

    def create_presets_file(self, path: str) -> None:
        """Creates and saves a presets file."""
        self.preset_data = {
            "paths": {
                "input_path": "",
                "output_path": ""
            }
        }
        # Check if the preset directory exists
        if not os.path.exists(self.preset_dir_path):
            Helper.create_dir(self.preset_dir_path)
        # Check if the preset file exists
        if not os.path.exists(path):
            Helper.save_file(path, self.preset_data)

    def load_presets(self) -> None:
        """Loads the presets from the file."""
        if os.path.exists(self.get_preset_path()):
            # Load the preset data from the currently selected preset file
            with open(os.path.join(self.preset_dir_path, f"{self.get_selected_preset()}.json"), "r") as f:
                self.preset_data = json.load(f)
        else:
            # If the preset file doesn't exist, create it
            self.create_presets_file()
            # * LOGGING
            print(f"New preset file created at {self.get_preset_path()}")

    def get_paths(self):
        """Loads all the Settings from a file and sets the filepaths to the corresponding entryfields."""
        # Deletes the entry fields
        self.app.InputEntry.delete(0, tk.END)
        self.app.OutputEntry.delete(0, tk.END)
        # Get the paths from the preset data
        self.app.InputEntry.insert(0, self.preset_data["paths"]["input_path"])
        self.app.OutputEntry.insert(0, self.preset_data["paths"]["output_path"])

    def set_paths(self, input_path: str, output_path: str) -> None:
        """Sets and saves the input and output paths."""
        self.preset_data["paths"]["input_path"] = input_path
        self.preset_data["paths"]["output_path"] = output_path
        Helper.save_file(self.get_preset_path(), self.preset_data)

    def on_preset_change(self, sel_preset) -> None:
        """Handles the event when the preset is changed."""
        # Try update the selected preset variable and save
        try:
            self.selected_preset.set(sel_preset)
            self.set_presets()  # Update the presets
            # * LOGGING
            print("Preset changed to:", sel_preset)
            # Load the current preset file
            self.load_presets()
            # Load the paths from the preset file
            self.get_paths()

        except ValueError as e:
            print(f"Error: {e}")

    def get_selected_preset(self) -> str:
        """Returns the currently selected preset."""
        return self.selected_preset.get()

    def set_presets(self) -> None:
        """Sets and saves the presets."""
        # Check if the selected preset is in the list of known presets
        if self.get_selected_preset() in self.presets:
            # If it is, set the presets to the data variable
            self.settings_data["preset_menu"] = {
                "selected_preset": self.get_selected_preset(), # Get selected preset as a string
                "presets": self.presets
            }
        else:
            raise ValueError(f"Preset '{self.get_selected_preset()}' is already known.")
        
        # Save the presets to the settings file
        Helper.save_file(self.settings_path, self.settings_data)

    def add_preset(self, preset:str) -> None:
        """Adds a new preset to the list of presets and saves it."""
        # Check if the preset is already in the list
        if not preset:
            raise ValueError("Preset name cannot be empty.")
        else:
            if preset not in self.presets:
                # If not, add it to the list and save
                self.presets.append(preset)
                # * LOGGING
                print(f"Added '{preset}' to the presets.")
                # Save the updated presets to the settings file
                self.set_presets()
                # Delete the entry field
                self.app.presetEntry.delete(0, tk.END)
                # Create new file for the new preset
                self.create_presets_file(self.get_preset_path(f"{preset}.json"))
                # Update the preset menu
                self.app.update_preset_menu()
                # Load the new preset file
                self.on_preset_change(preset)
            else:
                raise ValueError(f"Preset '{preset}' already exists.")

    def delete_preset(self, preset: str) -> None:
        """Deletes a preset from the list and saves it."""
        # Check if the preset is in the list
        if not preset:
            raise ValueError("Preset name cannot be empty.")
        else:
            if self.get_selected_preset() == preset:
                # If the currently selected preset is the one to be deleted, set it to the next one
                next_index = (self.presets.index(preset) + 1) % len(self.presets)
                self.selected_preset.set(self.presets[next_index])

            if preset in self.presets:
                # If it is, remove it from the list and save
                self.presets.remove(preset)
                # Save the updated presets to the settings file
                self.set_presets()
                # Delete the entry field
                self.app.presetEntry.delete(0, tk.END)
                # Update the preset menu
                self.app.update_preset_menu()
                # Delete the old preset file
                os.remove(self.get_preset_path(f"{preset}.json"))
                # * LOGGING
                print(f"Deleted preset:  {preset} & file: '{preset}.json'.")
                # Load the new preset file
                self.on_preset_change(self.get_selected_preset())
            else:
                raise ValueError(f"Preset '{preset}' does not exist.")

