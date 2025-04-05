# Settings Manager Class
import tkinter as tk
from tkinter import ttk
import os
import json
from HelperClass import Helper




class SettingsManager:
    """Handles loading, saving, and managing settings."""    
    def __init__(self, app, settings_path="./data/settings.json") -> None:
        self.app = app  # Store the App instance
        self.settings_path = settings_path
        self.settings_data = {}

        self.presets = ("Default", )
        self.selected_preset = tk.StringVar(value=self.presets[0])

        # Ensure the settings are loaded at the beginning
        self.load_settings()

    def create_settings_file(self) -> None:
        """Creates the settings file if it doesn't exist."""
        settings_path = "test"
        if not os.path.exists(self.settings_path):
            Helper.create_dir(self.settings_path)
            self.settings_data = {
                "paths": {
                    "input_path": "",
                    "output_path": ""
                }
            }
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
        self.settings_data["paths"]["input_path"] = input_path
        self.settings_data["paths"]["output_path"] = output_path
        Helper.save_file(self.settings_path, self.settings_data)

    def get_selected_preset(self) -> str:
        """Returns the currently selected preset."""
        return self.selected_preset.get()

    def set_selected_preset(self, preset: str) -> None:
        """Sets and saves the selected preset."""
        print(preset)
        print(self.presets)
        if preset in self.presets:
            self.selected_preset.set(preset)
            self.set_preset_menu()
        else:
            raise ValueError(f"Preset '{preset}' is already known.")

    # def get_preset_menu(self) -> dict:
    #     """Returns the options menu settings."""
    #     return self.settings_data.get("preset_menu", {})

    def set_preset_menu(self) -> None:
        """Sets and saves the preset menu settings."""
        options = {
            "presets": self.presets,
            "selected_preset": self.selected_preset.get()
        }
                
        self.settings_data["preset_menu"] = options
        Helper.save_file(self.settings_path, self.settings_data)

    # def add_preset(self, add_name: str, entry_widget: ttk.Entry) -> None:
    #     """Adds a new preset to the list and saves it."""
    #     presets_list = list(self.presets)
    #     if not add_name:
    #         raise ValueError("No value in datafield!")
    #     else:
    #         # Check if the name already exists
    #         if add_name in presets_list:
    #             raise ValueError (f"Preset '{add_name}' already exists.")
    #         else:
    #             # Add the new name to the list and save it
    #             presets_list.append(add_name)
    #             self.presets = tuple(presets_list)
    #             self.set_preset_menu()
    #             entry_widget.delete(0, tk.END)

                

    #             # * LOGGING
    #             print(f"Added '{add_name}' to the Presets.")
        
    # def delete_preset(self, entry_widget: ttk.Entry) -> None:
    #     presets_list = list(self.presets)
    #     entryfield_preset = entry_widget.get()

    #     # Remove preset, that was typed in the entryfield, if it matches
    #     if entryfield_preset:
    #         if entryfield_preset in presets_list:
    #             # If the entryfield has a correct string, delete it
    #             presets_list.remove(entryfield_preset)
    #             self.presets = tuple(presets_list)
    #             self.set_preset_menu()
    #             # Update Optionsmenu
    #             self.update_preset_option_menu()
    #             # Delete Entrywidget
    #             entry_widget.delete(0, tk.END)
    #             # * LOGGING
    #             print(f"Deleted '{entryfield_preset}' from the Presets.")
    #         else:
    #             raise ValueError(f"'{entryfield_preset}' is not in the Preset-List!")
    #     else:
    #         raise ValueError("Nothing to delete...")

