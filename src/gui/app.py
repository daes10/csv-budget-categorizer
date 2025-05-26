# system imports
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# local imports
from .window_manager import WindowManager
from ..classes import SettingsManager
from ..classes import PresetManager
from ..classes import DataManager
from ..utils import FileDialogHelper 
from ..utils.logging import logger

class App:
    """Main Application Class"""
    def __init__(self, main, monitor_idx=None) -> None:
        # Log application startup
        logger.info("Application is starting ...")

        self.main = main
        self.main.title("CSV Formatter")
        self.main.iconbitmap('resources/img/format_icon.ico')

        # Initialize window manager
        self.window_manager = WindowManager(self, monitor_idx)

        # Default settings
        self.settings_path = "./data/settings.json"
        self.data_path = "./data/data.json"

        # Initialize settings manager
        self.settings_manager = SettingsManager(self, self.settings_path)

        # Initialize preset manager
        self.preset_manager = PresetManager(self, self.settings_path)

        # Create GUI components
        self.create_widgets()

        # Initialize data manager
        self.data_manager = DataManager(app=self)
        logger.debug(self.data_manager)

        # Initialize file dialog helper
        self.file_dialog_helper = FileDialogHelper() 

    def create_widgets(self) -> None:
        """Creates the main GUI components."""
        # Frame for the bankoption
        bankFrame = ctk.CTkFrame(self.main)
        bankFrame.pack(fill="both", expand=False, padx=10, pady=5)

        ## Bank Option
        bankoption = ctk.CTkLabel(bankFrame, text="Bank:")
        bankoption.pack(padx=5, pady=5, side="left")



        # Frame for the csv paths
        csvPaths = ctk.CTkFrame(self.main)
        csvPaths.pack(fill="both", expand=False, padx=10, pady=5)

        ## Input Path
        InputLabel = ctk.CTkLabel(csvPaths, text="CSV-Einlesedatei:")
        InputLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.InputEntry = ctk.CTkEntry(csvPaths)
        self.InputEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileInput = ctk.CTkButton(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(self.InputEntry))
        btnFileInput.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        ## Output Path
        OutputLabel = ctk.CTkLabel(csvPaths, text="CSV-Ausgabepfad:")
        OutputLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.OutputEntry = ctk.CTkEntry(csvPaths)
        self.OutputEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        csvPaths.columnconfigure(1, weight=1)
        btnFileOutput = ctk.CTkButton(csvPaths, text="Datei auswählen", command=lambda: self.file_dialog_helper.open_fileDialog(self.OutputEntry))
        btnFileOutput.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        ## Load the paths from the current preset
        self.preset_manager.get_paths()  # Load the paths from the current preset
        
        ## Save Button
        btnSavePaths = ctk.CTkButton(csvPaths, text="Speichert Pfade", command=lambda: self.preset_manager.set_paths(self.InputEntry.get(), self.OutputEntry.get()))
        btnSavePaths.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    



        # Frame for the Input categories
        inputFrame = ctk.CTkFrame(self.main)
        inputFrame.pack(fill="both", expand=True, padx=10, pady=5)

        ## Add an Input Category
        btnAddCategoryInput = ctk.CTkButton(inputFrame, text="Kategorie hinzufügen", command=lambda: self.data_manager.add_category(self.treeInput))
        btnAddCategoryInput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Input Category
        btnDeleteCategoryInput = ctk.CTkButton(inputFrame, text="Kategorie löschen", command=lambda: self.data_manager.delete_category(self.treeInput))
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
        outputFrame = ctk.CTkFrame(self.main)
        outputFrame.pack(fill="both", expand=True, padx=10, pady=5)

        ## Add an Output Category
        btnAddCategoryOutput = ctk.CTkButton(outputFrame, text="Kategorie hinzufügen", command=lambda: self.data_manager.add_category(self.treeOutput))
        btnAddCategoryOutput.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ## Delete an Output Category
        btnDeleteCategoryOutput = ctk.CTkButton(outputFrame, text="Kategorie löschen", command=lambda: self.data_manager.delete_category(self.treeOutput))
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
        saveFrame = ctk.CTkFrame(self.main)
        saveFrame.pack(fill="both", expand=False, padx=10, pady=5)

        ## Save all Categories
        btnSaveCategories = ctk.CTkButton(saveFrame, text="Speichere Kategorien", command=lambda: self.data_manager.save_all_treeviews(self.treeInput, self.treeOutput))
        btnSaveCategories.pack(padx=5, pady=5, side="top")



        # Frame for presets
        presetsFrame = ctk.CTkFrame(self.main)
        presetsFrame.pack(fill="both", expand=True, padx=10, pady=5)
        ## Label entry presetname
        settingsLabel = ctk.CTkLabel(presetsFrame, text="Name: ")
        settingsLabel.pack(padx=5, pady=5, side="left")

        ## Entryfield for saved settings
        self.presetEntry = ctk.CTkEntry(presetsFrame)
        self.presetEntry.pack(padx=5, pady=5, side="left", fill="x", ipadx=100)

        ## Add preset
        self.btnAddPreset = ctk.CTkButton(presetsFrame, text="Hinzufügen", command=lambda: self.preset_manager.add_preset(self.presetEntry.get()))
        self.btnAddPreset.pack(padx=5, pady=5, side="left")

        ## Delete preset
        self.btnDelPreset = ctk.CTkButton(presetsFrame, text="Löschen", command=lambda: self.preset_manager.delete_preset(self.presetEntry.get()))
        self.btnDelPreset.pack(padx=5, pady=5, side="left")

        ## Option menu
        self.presetMenu = ctk.CTkOptionMenu(presetsFrame, # window frame
                                           variable=self.preset_manager.selected_preset, # selected preset at the moment
                                           values=self.preset_manager.presets, # a list of all presets ("*"" makes a tuple out of the list)
                                           command=self.preset_manager.on_preset_change  # Callback for when the preset changes
                                           )
        self.presetMenu.pack(padx=5, pady=5, ipadx=20, side="right", expand=True, anchor="w")

        ## Label preset menu
        presetLabel = ctk.CTkLabel(presetsFrame, text="Select Preset: ")
        presetLabel.pack(padx=5, pady=5, side="right", expand=False)



        # Keyboard shortcut bindings

        ## Bind the delete key to all treeviews
        self.main.bind_class("Treeview", "<Delete>", self.kb_tree_delete_row)

        # * DEBUGGING
        logger.debug("Widgets created...")

    def update_preset_menu(self) -> None:
        """Update the OptionMenu with the latest presets."""
        logger.debug("Update preset optionsmenu...")
        # Update optionmenu
        self.presetMenu.configure(values=self.preset_manager.presets)
        
        # Set the current preset to the newly optionmenu
        current_preset = self.preset_manager.get_selected_preset()
        if current_preset in self.preset_manager.presets:
            self.presetMenu.set(current_preset)
        else:
            logger.critical(f"Failed to update preset option menu: the current preset '{current_preset}' is not among the available presets.")
            raise ValueError(f"Failed to update preset option menu: the current preset '{current_preset}' is not among the available presets.")
        logger.debug("Preset optionsmenu updated.")



    # Methods for Keyboard shortcuts

    def kb_tree_delete_row(self, event) -> None:
        """Handles the delete key event for treeviews."""
        if event.keysym == "Delete":
            # Check which treeview is focused and delete the selected item
            if self.main.focus_get() == self.treeInput:
                self.data_manager.delete_category(self.treeInput)
            elif self.main.focus_get() == self.treeOutput:
                self.data_manager.delete_category(self.treeOutput)
