# system imports
import os
import json
from tkinter import ttk
from tkinter import messagebox

# local imports
from ..utils import Helper
from ..utils.logging import logger

class DataManager:
    """Handles loading, saving, and managing settings."""
    def __init__(self, app, data_path="./data/data.json"):
        self.app = app  # Store the App instance
        self.data_path = data_path
        self.data_data = {}

        # Ensure the data is loaded at the start
        self.load_categories()
    
        logger.debug(f"{self.__str__()}")

    def __str__(self) -> str:
        """Returns a string representation of the DataManager instance."""
        return f"DataManager: \n  -> data_path= {self.data_path},\n  -> data_data= {self.data_data}"

    def create_data_file(self) -> None:
        """Creates the data-json file if it doesn't exist."""
        if not os.path.exists(self.data_path):
            logger.info("Create data path...")
            Helper.create_dir(self.data_path)
            logger.info("Create data file with config...")
            Helper.save_file(self.data_path, self.data_data)

    def save_all_treeviews(self, treeInput: ttk.Treeview, treeOutput: ttk.Treeview) -> None:
        """Saves both input and output categories."""
        self.save_treeview_data(treeInput, "input")
        self.save_treeview_data(treeOutput, "output")
        logger.info("Saved treeview data to current preset.")

    def save_treeview_data(self, treeview: ttk.Treeview, switch: str = "input" or "output") -> None:
        """Saves the data from the Treeview widget to a JSON file."""
        # List to hold all rows of data
        data_list = [] # List of dictionaries
        
        # * DEBUGGING
        # print(treeview["columns"][0])
        
        # Iterate through all items in the Treeview
        for item_id in treeview.get_children():
            # Get the values of the current item
            row_list = treeview.item(item_id)["values"]
            
            # Create a dictionary for the data
            row_dict = {
                str(treeview["columns"][0]): row_list[0],
                str(treeview["columns"][1]): row_list[1],
                str(treeview["columns"][2]): row_list[2],
                str(treeview["columns"][3]): row_list[3],
                str(treeview["columns"][4]): float(row_list[4]),
                str(treeview["columns"][5]): float(row_list[5])
            }
            # Append the dictionary to the list
            data_list.append(row_dict)

        # * DEBUGGING
        # print("Data List:" + str(data_list))

        # Save the data to the JSON file
        if switch == "input":
            self.data_data["input_categories"] = data_list
        
        if switch == "output":
            self.data_data["output_categories"] = data_list

        # Save the data to the current Preset JSON file
        preset_path = self.app.preset_manager.get_preset_path()
        Helper.update_json_file(preset_path, self.data_data)

        # * DEBUGGING
        # print(json.dumps(self.data_data, indent=4))
    
    def add_category(self, table_name: ttk.Treeview) -> None:
        """Adds a new category to the list with default values."""
        table_name.insert("", 0, values=("Kategorie", "", "01.01.2023", "31.12.2023", 0.0, 1000.0))
        logger.debug("Insert a new row in the Treeview...")

    def delete_category(self, treeview: ttk.Treeview) -> None:
        """Deletes the selected categories from the list."""
        selected_items = treeview.selection()

        if selected_items:
            next_item = treeview.next(selected_items[-1])
            prev_item = treeview.prev(selected_items[0])

            if next_item:
                treeview.selection_set(next_item)
                treeview.focus(next_item)

            if prev_item:
                treeview.selection_set(prev_item)
                treeview.focus(prev_item)

            # Delete all selected item/s
            for item in selected_items:
                treeview.delete(item)

                logger.debug("Delete row/s in the treeview...")
                
        # if no items are selected, give the user some feedback
        else:
            logger.warning("No item selected to delete!")
            # Opens a messagebox to inform the user
            messagebox.showinfo("Info", "Please choose first a row to delete")

    def load_categories(self) -> None:
        """Loads categories from the JSON file."""
        if os.path.exists(self.data_path):
            logger.debug("Loading treeview data from file...")
            with open(self.data_path, "r") as f:
                self.data_data = json.load(f)
            
            # Clear the treeview before loading new data
            logger.debug("Clearing data from the treeviews...")
            self.app.treeInput.delete(*self.app.treeInput.get_children())
            self.app.treeOutput.delete(*self.app.treeOutput.get_children())

            # Load categories into both treeviews
            logger.debug("Loading data into treeviews...")
            for catItem in self.data_data.get("input_categories", []):
                self.app.treeInput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))

            for catItem in self.data_data.get("output_categories", []):
                self.app.treeOutput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))
            logger.debug("Treeviews updated!")
        else:
            self.create_data_file()