import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os
from ttkthemes import ThemedTk  # importing ThemedTk libary



class DataManager:
    """Handles loading, saving, and managing settings."""    
    def __init__(self, app, settings_path="./data/settings.json", data_dir="./data", data_path="./data/data.json") -> None:
        self.app = app  # Store the app instance
        self.settings_path = settings_path
        self.settings_data = {}
        self.data_dir = data_dir
        self.data_path = data_path
        self.data_data = {}

        # Ensure the settings file exists
        self.create_settings_file()

        # Ensure the settings are loaded at the beginning
        self.load_settings()

    
    def create_dir(self, dir_path: str) -> None:
        """Creates the data directory if it doesn't exist."""
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def create_data_file(self) -> None:
        """Creates the data json file if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            self.create_dir(self.data_dir)
        if not os.path.exists(self.data_path):
            #self.data_data = {}
            self.save(self.data_path, self.data_data)

    def create_settings_file(self) -> None:
        """Creates the settings file if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            self.create_dir(self.data_dir)
        if not os.path.exists(self.settings_path):
            self.settings_data = {
                "paths": {
                    "input_path": "",
                    "output_path": ""
                }
            }
            self.save(self.settings_path, self.settings_data)
    


    def load_settings(self) -> None:
        """Loads settings from the JSON file."""
        if os.path.exists(self.settings_path):
            with open(self.settings_path, "r") as f:
                self.settings_data = json.load(f)
        else:
            self.create_settings_file()



    def save(self, file_path: str, file_data: dict) -> None:
        """Saves a file."""
        with open(file_path, "w") as f:
            json.dump(file_data, f, indent=4)

    def save_all_categories(self, treeInput: ttk.Treeview, treeOutput: ttk.Treeview) -> None:
        """Saves both input and output categories."""
        self.save_treeview_data(treeInput, "input")
        self.save_treeview_data(treeOutput, "output")

    def save_treeview_data(self, treeview: ttk.Treeview, switch: str = "input" or "output") -> None:
        """Saves the data from the Treeview widget to a JSON file."""
        # List to hold all rows of data
        data_list = [] # List of dictionaries
        print(treeview["columns"][0])
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
            print(self.data_data)
            self.data_data["input_categories"] = data_list
            self.save(self.data_path, self.data_data)
        
        if switch == "output":
            self.data_data["output_categories"] = data_list
            self.save(self.data_path, self.data_data)

        # * DEBUGGING
        # print(json.dumps(self.data_data, indent=4))




    def get_paths(self, entry_input: ttk.Entry, entry_output: ttk.Entry):
        """Loads all the Settings from a file and sets the filepaths to the corresponding entryfields."""
        self.load_settings()
        entry_input.insert(0, self.settings_data["paths"]["input_path"])
        entry_output.insert(0, self.settings_data["paths"]["output_path"])

    def set_paths(self, input_path: str, output_path: str) -> None:
        """Sets and saves the input and output paths."""
        self.settings_data["paths"]["input_path"] = input_path
        self.settings_data["paths"]["output_path"] = output_path
        self.save(self.settings_path, self.settings_data)







class App:
    """Main Application Class"""
    def __init__(self, main) -> None:
        self.main = main
        self.main.title("CSV Formatter")
        self.main.iconbitmap('./img/format_icon.ico')
        self.center_window(1200, 1000, self.main)
        self.main.resizable(True, True)

        # Initialize settings manager
        self.data_manager = DataManager(self)

        # Initialize file dialog helper
        self.file_dialog_helper = FileDialogHelper()

        # Create GUI components
        self.create_widgets()

        # Ensure the data are loaded at the beginning
        self.load_categories()

    def center_window(self, window_width, window_height, window_name) -> None:
        """Sets the position of the window to the center of the screen"""
        # Update the "requested size" from geometry manager
        window_name.update_idletasks()

        # Get the requested size of the window
        screen_width = window_name.winfo_screenwidth()
        screen_height = window_name.winfo_screenheight()

        # find the x and y axis for the window
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Positioning of the defined window
        window_name.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


    def create_widgets(self) -> None:
        """Creates the main GUI components."""
        # Frame for the bankoption
        bankFrame = ttk.LabelFrame(self.main, text="Bankselektion", labelanchor="nw")
        bankFrame.pack(fill="both", expand="no", padx=10, pady=5)

        ## Bank Option
        bankoption = ttk.Label(bankFrame, text="Bank:")
        bankoption.pack(padx=5, pady=5, side="left")



        # Frame for the csv paths
        csvPaths = ttk.LabelFrame(self.main, text="Dateipfade", labelanchor="nw")
        csvPaths.pack(fill="both", expand="no", padx=10, pady=5)

        ## Input Path
        InputLabel = ttk.Label(csvPaths, text="CSV-Einlesedatei:")
        InputLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        InputEntry = ttk.Entry(csvPaths)
        InputEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileInput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(InputEntry))
        btnFileInput.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        ## Output Path
        OutputLabel = ttk.Label(csvPaths, text="CSV-Ausgabepfad:")
        OutputLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        OutputEntry = ttk.Entry(csvPaths)
        OutputEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileOutput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(OutputEntry))
        btnFileOutput.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ## Load paths from settings.json if it exists
        self.data_manager.get_paths(InputEntry, OutputEntry)

        ## Save button
        btnSavePaths = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: self.data_manager.set_paths(InputEntry.get(), OutputEntry.get()))
        btnSavePaths.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    


        # Frame for the Input categories
        inputFrame = ttk.LabelFrame(self.main, text="Einnahmen", labelanchor="nw")
        inputFrame.pack(fill="both", expand="yes", padx=10, pady=5)

        ## Add an Input Category
        btnAddCategoryInput = ttk.Button(inputFrame, text="Kategorie hinzufügen", command=lambda: self.add_category(self.treeInput))
        btnAddCategoryInput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Input Category
        btnDeleteCategoryInput = ttk.Button(inputFrame, text="Kategorie löschen", command=lambda: self.delete_category(self.treeInput))
        btnDeleteCategoryInput.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
        ## Create the Input Treeview widget
        self.treeInput = ttk.Treeview(inputFrame, columns=("category", "filters", "dateFrom", "dateTo", "minValue", "maxValue"), show="headings")
        self.treeInput.heading("category", text="Kategorie")
        self.treeInput.heading("filters", text="Suchbegriff")
        self.treeInput.heading("dateFrom", text="Datum von")
        self.treeInput.heading("dateTo", text="Datum bis")
        self.treeInput.heading("minValue", text="Min. Betrag")
        self.treeInput.heading("maxValue", text="Max. Betrag")
        self.treeInput.grid(row=1, column=0, padx=5, pady=5, columnspan=8, sticky="nsew")
        inputFrame.columnconfigure(0, weight=1)
        inputFrame.columnconfigure(1, weight=1)
        inputFrame.columnconfigure(2, weight=40)
        inputFrame.rowconfigure(1, weight=1)

        ## Configure the columns in the Treeview widget
        for col in self.treeInput["columns"]:
            self.treeInput.column(col, width=100, stretch=True, anchor="center")



        # Frame for the output categories
        outputFrame = ttk.LabelFrame(self.main, text="Ausgaben", labelanchor="nw")
        outputFrame.pack(fill="both", expand="yes", padx=10, pady=5)

        ## Add an Output Category
        btnAddCategoryOutput = ttk.Button(outputFrame, text="Kategorie hinzufügen", command=lambda: self.add_category(self.treeOutput))
        btnAddCategoryOutput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Output Category
        btnDeleteCategoryOutput = ttk.Button(outputFrame, text="Kategorie löschen", command=lambda: self.delete_category(self.treeOutput))
        btnDeleteCategoryOutput.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ## Create the Output Treeview widget
        self.treeOutput = ttk.Treeview(outputFrame, columns=("category", "filters", "dateFrom", "dateTo", "minValue", "maxValue"), show="headings")
        self.treeOutput.heading("category", text="Kategorie")
        self.treeOutput.heading("filters", text="Suchbegriff")
        self.treeOutput.heading("dateFrom", text="Datum von")
        self.treeOutput.heading("dateTo", text="Datum bis")
        self.treeOutput.heading("minValue", text="Min. Betrag")
        self.treeOutput.heading("maxValue", text="Max. Betrag")
        self.treeOutput.grid(row=1, column=0, padx=5, pady=5, columnspan=4, sticky="nsew")
        outputFrame.columnconfigure(0, weight=1)
        outputFrame.columnconfigure(1, weight=1)
        outputFrame.columnconfigure(2, weight=40)
        outputFrame.rowconfigure(1, weight=1)

        ## Configure the columns in the Treeview widget
        for col in self.treeOutput["columns"]:
            self.treeOutput.column(col, width=100, stretch=True, anchor="center")



        # Frame for Saving the categories
        saveFrame = ttk.LabelFrame(self.main, text="Einstellungen", labelanchor="nw")
        saveFrame.pack(fill="both", expand="no", padx=10, pady=5)

        ## Save all Categories
        btnSaveCategories = ttk.Button(saveFrame, text="Kategorien speichern", command=lambda: self.data_manager.save_all_categories(self.treeInput, self.treeOutput))
        btnSaveCategories.pack(padx=5, pady=5, side="left")



    def add_category(self, table_name: ttk.Treeview) -> None:
        """Adds a new category to the list with default values."""
        table_name.insert("", 0, values=("Kategorie", "", "01.01.2023", "31.12.2023", 0.0, 1000.0))

    def delete_category(self, table_name: ttk.Treeview) -> None:
        """Deletes the selected category from the list."""
        selected_item = table_name.selection()
        if selected_item:
            for item in selected_item:
                table_name.delete(item)
        else:
            # * LOGGING
            print("No item selected to delete.")
            # Opens a messagebox to inform the user
            tk.messagebox.showinfo("Info", "Bitte wähle erst eine Kategorie aus, um sie zu löschen.")     

    def load_categories(self) -> None:
        """Loads categories from the JSON file."""
        if os.path.exists(self.data_manager.data_path):
            with open(self.data_manager.data_path, "r") as f:
                self.data_manager.data_data = json.load(f)
            
            # Clear the treeview before loading new data
            self.treeInput.delete(*self.treeInput.get_children())
            self.treeOutput.delete(*self.treeOutput.get_children())

            # Load categories into both treeviews
            for catItem in self.data_manager.data_data.get("input_categories", []):
                self.treeInput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))

            for catItem in self.data_manager.data_data.get("output_categories", []):
                self.treeOutput.insert("", 0, values=(catItem["category"], catItem["filters"], catItem["dateFrom"], catItem["dateTo"], catItem["minValue"], catItem["maxValue"]))
        else:
            self.data_manager.create_data_file()




class FileDialogHelper:
    """A helper class for file dialog operations"""
    def __init__(self):
        ...
    
    def open_fileDialog(self, widget: ttk.Entry) -> str:
        """Opens a file dialog to select a CSV file and inserts the selected file path into the given widget."""
        filepath = filedialog.askopenfilename(
            title="Öffne CSV-Datei",
            initialdir="./",
            filetypes=[("CSV files", "*.csv")]
        )
        widget.delete(0, tk.END)
        widget.insert(0, filepath)
        return filepath



if __name__ == "__main__":
    main_window = tk.Tk()  # Using Tk for a basic window (optional)
    # main_window = ThemedTk(theme="arc")  # Using ThemedTk for a themed window
    app = App(main_window)
    main_window.mainloop() # Mainloop from "main"-Window