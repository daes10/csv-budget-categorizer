import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk  # importing ThemedTk libary
from SettingsManager import SettingsManager
from DataManager import DataManager
from FileDialogHelper import FileDialogHelper



class App:
    """Main Application Class"""
    def __init__(self, main) -> None:
        self.main = main
        self.main.title("CSV Formatter")
        self.main.iconbitmap('./img/format_icon.ico')
        self.center_window(1200, 1000, self.main)
        self.main.resizable(True, True)

        # Initialize settings manager
        self.settings_manager = SettingsManager()

        # Create GUI components
        self.create_widgets()

        # Initialize data manager
        self.data_manager = DataManager(app=self)

        # Initialize file dialog helper
        self.file_dialog_helper = FileDialogHelper()


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
        self.settings_manager.get_paths(InputEntry, OutputEntry)

        ## Save button
        btnSavePaths = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: self.settings_manager.set_paths(InputEntry.get(), OutputEntry.get()))
        btnSavePaths.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    


        # Frame for the Input categories
        inputFrame = ttk.LabelFrame(self.main, text="Einnahmen", labelanchor="nw")
        inputFrame.pack(fill="both", expand="yes", padx=10, pady=5)

        ## Add an Input Category
        btnAddCategoryInput = ttk.Button(inputFrame, text="Kategorie hinzufügen", command=lambda: self.data_manager.add_category(self.treeInput))
        btnAddCategoryInput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Input Category
        btnDeleteCategoryInput = ttk.Button(inputFrame, text="Kategorie löschen", command=lambda: self.data_manager.delete_category(self.treeInput))
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
        btnAddCategoryOutput = ttk.Button(outputFrame, text="Kategorie hinzufügen", command=lambda: self.data_manager.add_category(self.treeOutput))
        btnAddCategoryOutput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Output Category
        btnDeleteCategoryOutput = ttk.Button(outputFrame, text="Kategorie löschen", command=lambda: self.data_manager.delete_category(self.treeOutput))
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
        btnSaveCategories = ttk.Button(saveFrame, text="Kategorien speichern", command=lambda: self.data_manager.save_all_treeviews(self.treeInput, self.treeOutput))
        btnSaveCategories.pack(padx=5, pady=5, side="left")







if __name__ == "__main__":
    main_window = tk.Tk()  # Using Tk for a basic window (optional)
    # main_window = ThemedTk(theme="arc")  # Using ThemedTk for a themed window
    app = App(main_window)
    main_window.mainloop() # Mainloop from "main"-Window