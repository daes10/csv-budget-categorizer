import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os



class SettingsManager:
    """Handles loading, saving, and managing settings."""    
    def __init__(self, settings_file="./data/settings.json") -> None:
        self.settings_file = settings_file
        self.settings = {}

        # Ensure the settings file exists
        self.create_settings_file()

        # Ensure the settings are loaded at the beginning
        self.load_settings()

    def create_settings_file(self) -> None:
        """Creates the settings file if it doesn't exist."""
        if not os.path.exists("./data"):
            os.makedirs("./data")
        if not os.path.exists(self.settings_file):
            self.settings = {
                "paths": {
                    "input_path": "",
                    "output_path": ""
                }
            }
            self.save_settings()
    
    def load_settings(self) -> None:
        """Loads settings from the JSON file."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        else:
            self.create_settings_file()

    def save_settings(self) -> None:
        """Saves the current settings to the JSON file."""
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_paths(self, entry_input: ttk.Entry, entry_output: ttk.Entry):
        """Loads all the Settings from a file and sets the filepaths to the corresponding entryfields."""
        self.load_settings()
        entry_input.insert(0, self.settings["paths"]["input_path"])
        entry_output.insert(0, self.settings["paths"]["output_path"])

    def set_paths(self, input_path: str, output_path: str) -> None:
        """Sets and saves the input and output paths."""
        self.settings["paths"]["input_path"] = input_path
        self.settings["paths"]["output_path"] = output_path
        self.save_settings()



class App:
    """Main Application Class"""
    def __init__(self, main) -> None:
        self.main = main
        self.main.title("CSV Formatter")
        self.main.iconbitmap('./img/format_icon.ico')
        self.centering_window(1000, 600, self.main)

        # Initialize settings manager
        self.settings_manager = SettingsManager()

        # Initialize file dialog helper
        self.file_dialog_helper = FileDialogHelper()

        # Create GUI components
        self.create_widgets()

    def centering_window(self, window_width, window_height, window_name) -> None:
        """Sets the position of the window to the center of the screen"""
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
        bankFrame = ttk.LabelFrame(self.main, text="Bankselektion", labelanchor="n")
        bankFrame.pack(fill="both", expand="no", padx=10, pady=5)

        ## Bank Option
        bankoption = ttk.Label(bankFrame, text="Bank:")
        bankoption.pack(padx=5, pady=5, side="left")

        # Frame for the csv paths
        csvPaths = ttk.LabelFrame(self.main, text="Dateipfade", labelanchor="n")
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
        self.settings_manager.get_paths(InputEntry, OutputEntry)

        ## Save button
        saveBtn = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: self.settings_manager.set_paths(InputEntry.get(), OutputEntry.get()))
        saveBtn.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # Frame for the input categories
        inputFrame = ttk.LabelFrame(self.main, text="Einnahmen", labelanchor="n")
        inputFrame.pack(fill="both", expand="yes", padx=10, pady=5)

        ## Create the Treeview widget
        treeInput = ttk.Treeview(inputFrame, columns=("category", "filters", "dateFrom", "dateTo", "minValue", "maxValue"), show="headings")
        treeInput.heading("category", text="Kategorie")
        treeInput.heading("filters", text="Suchbegriff")
        treeInput.heading("dateFrom", text="Datum von")
        treeInput.heading("dateTo", text="Datum bis")
        treeInput.heading("minValue", text="Min. Betrag")
        treeInput.heading("maxValue", text="Max. Betrag")
        treeInput.pack(fill="both", expand="yes", padx=10, pady=5)

        ## Configure the columns in the Treeview widget
        for col in treeInput["columns"]:
            treeInput.column(col, width=100, stretch=True, anchor="center")

        # treeInput.insert()




        # frame for the output categories
        outputFrame = ttk.LabelFrame(self.main, text="Ausgaben", labelanchor="n")
        outputFrame.pack(fill="both", expand="yes", padx=10, pady=5)



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
    main_window = tk.Tk()
    app = App(main_window)
    main_window.mainloop() # Mainloop from "main"-Window