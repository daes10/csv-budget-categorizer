import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk  # importing ThemedTk libary
from SettingsManager import *
from DataManager import DataManager
from FileDialogHelper import FileDialogHelper



class App:
    """Main Application Class"""
    def __init__(self, main) -> None:
        self.main = main
        self.main.title("CSV Formatter")
        self.main.iconbitmap('./img/format_icon.ico')
        self.center_window(1200, 900, self.main)
        self.main.resizable(True, True)

        # Default settings
        self.settings_path = "./data/settings.json"

        # Initialize settings manager
        self.settings_manager = SettingsManager(self, self.settings_path)
        # * DEBUGGING Settings Manager
        # print(self.settings_manager)

        # Initialize preset manager
        self.preset_manager = PresetManager(self, self.settings_path)
        # * DEBUGGING Preset Manager
        # print(self.preset_manager)

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
        bankFrame = ttk.LabelFrame(self.main, text="", labelanchor="nw")
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
        self.InputEntry = ttk.Entry(csvPaths)
        self.InputEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileInput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(self.InputEntry))
        btnFileInput.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        ## Output Path
        OutputLabel = ttk.Label(csvPaths, text="CSV-Ausgabepfad:")
        OutputLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.OutputEntry = ttk.Entry(csvPaths)
        self.OutputEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileOutput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(self.OutputEntry))
        btnFileOutput.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ## Load paths from settings.json if it exists
        self.preset_manager.get_paths()

        ## Save button
        btnSavePaths = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: self.preset_manager.set_paths(self.InputEntry.get(), self.OutputEntry.get()))
        btnSavePaths.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    


        # Frame for the Input categories
        inputFrame = ttk.LabelFrame(self.main, text="Einnahmen", labelanchor="n")
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
        outputFrame = ttk.LabelFrame(self.main, text="Ausgaben", labelanchor="n")
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
        saveFrame = ttk.Frame(self.main)
        saveFrame.pack(fill="both", expand="no", padx=10, pady=5)

        ## Save all Categories
        btnSaveCategories = ttk.Button(saveFrame, text="Daten Konvertieren", command=lambda: self.data_manager.save_all_treeviews(self.treeInput, self.treeOutput))
        btnSaveCategories.pack(padx=5, pady=5, side="top")



        # Frame for presets
        presetsFrame = ttk.LabelFrame(self.main, text="Presets", labelanchor="nw")
        presetsFrame.pack(fill="both", expand="no", padx=10, pady=5)

        ## Label entry presetname
        settingsLabel = ttk.Label(presetsFrame, text="Name: ")
        settingsLabel.pack(padx=5, pady=5, side="left")

        ## Entryfield for saved settings
        self.presetEntry = ttk.Entry(presetsFrame)
        self.presetEntry.pack(padx=5, pady=5, side="left", fill="x", ipadx=100)

        ## Add preset
        self.btnAddPreset = ttk.Button(presetsFrame, text="Hinzufügen", command=lambda: self.preset_manager.add_preset(self.presetEntry.get()))
        self.btnAddPreset.pack(padx=5, pady=5, side="left")

        ## Delete preset
        self.btnDelPreset = ttk.Button(presetsFrame, text="Löschen", command=lambda: self.preset_manager.delete_preset(self.presetEntry.get()))
        self.btnDelPreset.pack(padx=5, pady=5, side="left")

        ## Option menu
        self.presetMenu = ttk.OptionMenu(presetsFrame, # window frame
                                           self.preset_manager.selected_preset, # selected preset at the moment
                                           self.preset_manager.get_selected_preset(), # default start preset
                                           *self.preset_manager.presets, # a list of all presets ("*"" makes a tuple out of the list)
                                           direction="above", # direction of the menu
                                           command=self.preset_manager.on_preset_change  # Callback for when the preset changes
                                           )
        self.presetMenu.pack(padx=5, pady=5, ipadx=20, side="right", expand=True, anchor="w")

        ## Label preset menu
        presetLabel = ttk.Label(presetsFrame, text="Select Preset: ")
        presetLabel.pack(padx=5, pady=5, side="right", expand=False)


    def update_preset_menu(self) -> None:
        """Update the OptionMenu with the latest presets."""
        menu = self.presetMenu["menu"]
        menu.delete(0, "end")  # Clear the current options
        
        for preset in self.preset_manager.presets:
            # Use a lambda that calls on_preset_change with the preset name
            menu.add_command(label=preset, command=lambda value=preset: self.preset_manager.on_preset_change(value))       




if __name__ == "__main__":
    main_window = tk.Tk()  # Using Tk for a basic window (optional)
    # main_window = ThemedTk(theme="arc")  # Using ThemedTk for a themed window
    app = App(main_window)
    main_window.mainloop() # Mainloop from "main"-Window
    