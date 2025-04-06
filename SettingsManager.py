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
        settings_path = "test"
        if not os.path.exists(self.settings_path):
            Helper.create_dir(self.settings_path)
            self.settings_data = {
                "paths": {
                    "input_path": "",
                    "output_path": ""
                },
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

    def get_paths(self, entry_input: ttk.Entry, entry_output: ttk.Entry):
        """Loads all the Settings from a file and sets the filepaths to the corresponding entryfields."""
        self.load_settings()
        entry_input.insert(0, self.settings_data["paths"]["input_path"])
        entry_output.insert(0, self.settings_data["paths"]["output_path"])

    def set_paths(self, input_path: str, output_path: str) -> None:
        """Sets and saves the input and output paths."""
        self.settings_data["paths"]["input_path"] = input_path
        self.settings_data["paths"]["output_path"] = output_path
        Helper.save_file(self.settings_path, self.settings_data)


class PresetManager(SettingsManager):
    """Handles loading, saving, and managing presets."""
    def __init__(self, app, settings_path) -> None:
        super().__init__(app, settings_path) # Call the parent constructor and initialize the required properties

        # Define preset properties
        self.presets = ["Default", "Custom"]


        # Set the default preset if none is found in settings
        self.selected_preset = tk.StringVar(value=self.settings_data.get("preset_menu", {}).get("selected_preset") or self.presets[0])

        # If we're using the default value, save it to ensure it's properly stored
        if not self.settings_data.get("preset_menu", {}).get("selected_preset"):
            self.set_presets()  # Save the default preset

    def __str__(self) -> str:
        """Returns a string representation of the PresetManager instance."""
        return f"PresetManager: \n  -> presets= {self.presets},\n  -> selected_preset= {self.selected_preset.get()},\n  -> settings_path= {self.settings_path},\n  -> settings_data= {self.settings_data}"

    def on_preset_change(self, event) -> None:
        """Handles the event when the preset is changed."""
        print("Preset changed to:", event)
        # Update the selected preset variable and save
        self.selected_preset.set(event)
        self.set_presets()  # Update the presets
        # TODO: Implement the logic to handle preset changes
        

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
        
        # Save the presets to the settings file
        Helper.save_file(self.settings_path, self.settings_data)
        

    # def set_selected_preset(self, preset: str) -> None:
    #     """Sets and saves the selected preset."""
    #     print(preset)
    #     print(self.presets)
    #     if preset in self.presets:
    #         self.selected_preset.set(preset)
    #         self.set_preset_menu()
    #     else:
    #         raise ValueError(f"Preset '{preset}' is already known.")



    # def set_preset_menu(self) -> None:
    #     """Sets and saves the preset menu settings."""
    #     options = {
    #         "presets": self.presets,
    #         "selected_preset": self.selected_preset.get()
    #     }
                
    #     self.settings_data["preset_menu"] = options
    #     Helper.save_file(self.settings_path, self.settings_data)



