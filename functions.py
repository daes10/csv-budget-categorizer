import tkinter as tk
from tkinter import filedialog as fd
import json
import os


# This file contains functions that are used in the GUI


# create a function that will be called when the button is clicked
def button_clicked():
    print("Button clicked!")

# function to center the tkinter main window on the screen
def center_screen(mainWidth, mainHeight, windowName) -> None:
    # Get the screen dimension
    screenWidth = windowName.winfo_screenwidth()
    screenHeight = windowName.winfo_screenheight()

    # find the x and y axis for the window
    center_x = int(screenWidth / 2 - mainWidth / 2)
    center_y = int(screenHeight / 2 - mainHeight / 2)

    # Geometry of the main window
    windowName.geometry(f'{mainWidth}x{mainHeight}+{center_x}+{center_y}')


# Geometry of the main window
main_width = 1000
main_height = 600

# This function opens a file dialog to select a CSV file and inserts the selected file path into the given widget
def select_filepath(widget: tk.Tk) -> None:
    filename = fd.askopenfilename(
        title='Öffne CSV-Datei',
        initialdir='./',  # start directory in project folder
        filetypes=[('CSV files', '*.csv')])
    widget.delete(0, tk.END) # delete the current content
    widget.insert(0, filename)

def save_paths(input_path: str, output_path: str) -> None:
    # save the paths to a settings json file
    # check if the file exists
    if os.path.exists('./data/settings.json'):
        with open('./data/settings.json', 'r') as f:
            settingsJSON = json.load(f)
    else:
        settingsJSON = {}
    
    # create the paths dict
    paths = {
        "input_path": input_path,
        "output_path": output_path
    }
    # add the paths to the settings dict
    settingsJSON["paths"] = paths

    # save the settings to the json file
    with open("./data/settings.json", "w") as f:
        json.dump(settingsJSON, f, indent=4)

def create_settings() -> None:
    # create the settings folder if it does not exist
    if not os.path.exists("./data"):
        os.makedirs("./data")
    # create the settings json file if it does not exist
    if not os.path.exists("./data/settings.json"):
        # create the settings json file with default values
        settingsJSON = {}
        with open("./data/settings.json", "w") as f:
            json.dump(settingsJSON, f, indent=4)

# load the paths into the entry fields
def load_paths_to_entry(entry_Input: tk.Entry, entry_Output: tk.Entry) -> None:
    # load the paths from the settings json file
    if os.path.exists("./data/settings.json"):
        with open("./data/settings.json", "r") as f:
            settingsJSON = json.load(f)
        
        # ensure the "paths" key exists in the json file
        if "paths" not in settingsJSON:
            with open("./data/settings.json", "w") as f:
                settingsJSON["paths"] = {}
                json.dump(settingsJSON, f, indent=4)
        # check if the paths exist in the json file
        if "input_path" not in settingsJSON["paths"]:
            with open("./data/settings.json", "w") as f:
                settingsJSON["paths"]["input_path"] = ""
                json.dump(settingsJSON, f, indent=4)
        # check if the output path exists in the json file
        if "output_path" not in settingsJSON["paths"]:
            with open("./data/settings.json", "w") as f:
                settingsJSON["paths"]["output_path"] = ""
                json.dump(settingsJSON, f, indent=4)

        # load the paths into the entry fields
        entry_Input.delete(0, tk.END)
        entry_Input.insert(0, settingsJSON["paths"]["input_path"])
        entry_Output.delete(0, tk.END)
        entry_Output.insert(0, settingsJSON["paths"]["output_path"])
    else:
        # create the settings file if it does not exist
        create_settings()

