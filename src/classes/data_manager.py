# system imports
import os
import json
from tkinter import ttk
from tkinter import messagebox

# local imports
from ..utils import Helper


class DataManager:
    """Handles loading, saving, and managing settings."""
    def __init__(self, app, data_path="./data/data.json"):
        self.app = app  # Store the App instance
        self.data_path = data_path
        self.data_data = {}

        # Ensure the data is loaded at the start
        self.load_categories()
    

    def create_data_file(self) -> None:
        """Creates the "./data/data.json" json file if it doesn't exist."""
        if not os.path.exists(self.data_path):
            Helper.create_dir(self.data_path)
            Helper.save_file(self.data_path, self.data_data)

    def save_all_treeviews(self, treeInput: ttk.Treeview, treeOutput: ttk.Treeview) -> None:
        """Saves both input and output categories."""
        self.save_treeview_data(treeInput, "input")
        self.save_treeview_data(treeOutput, "output")

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

    def delete_category(self, treeview: ttk.Treeview) -> None:
        """Deletes the selected categories from the list."""
        selected_items = treeview.selection()

        # ? Here is still a small Bug: It's not possible to delete the last item in the List.
        # If there are selected items, delete them
        if selected_items:
            next_item = treeview.next(selected_items[-1])

            # If there is a next item, select it
            if next_item:
                treeview.selection_set(next_item)
                treeview.focus(next_item)

                # If more than one item is selected, delete all of them
                for item in selected_items:
                    # Delete the selected item/s
                    treeview.delete(item)

            # If there are no more items left, select the previous item
            else:
                prev_item = treeview.prev(selected_items[0])

                if prev_item:
                    treeview.selection_set(prev_item)
                    treeview.focus(prev_item)

                    # If more than one item is selected, delete all of them
                    for item in selected_items:
                        # Delete the selected item/s
                        treeview.delete(item)


                
        else:
            # * LOGGING
            print("No item selected to delete.")
            # Opens a messagebox to inform the user
            messagebox.showinfo("Info", "Bitte wähle erst eine Kategorie aus, um sie zu löschen.")

    def load_categories(self) -> None:
        """Loads categories from the JSON file."""
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                self.data_data = json.load(f)
            
            # Clear the treeview before loading new data
            self.app.treeInput.delete(*self.app.treeInput.get_children())
            self.app.treeOutput.delete(*self.app.treeOutput.get_children())

            # Load categories into both treeviews
            for catItem in self.data_data.get("input_categories", []):
                self.app.treeInput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))

            for catItem in self.data_data.get("output_categories", []):
                self.app.treeOutput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))
        else:
            self.create_data_file()