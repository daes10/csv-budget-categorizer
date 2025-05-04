# system imports
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors  # for centering the window

# local imports
from ..classes import SettingsManager
from ..classes import PresetManager
from ..classes import DataManager
from ..utils import FileDialogHelper


class App:
    """Main Application Class"""
    def __init__(self, main, monitor_idx=None) -> None:
        self.main = main
        self.monitor_idx = monitor_idx
        self.main.title("CSV Formatter")
        self.main.iconbitmap('resources/img/format_icon.ico')
        self.set_app_dpi_awareness()
        
        self.center_window(1200, 900, self.main)
        self.main.resizable(True, True)

        # * DEBUGGING
        print("Application is starting...")

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

        # select display by index or default to rightmost
        monitors = get_monitors()
        if self.monitor_idx is not None and 0 <= self.monitor_idx < len(monitors):
            monitor = monitors[self.monitor_idx]
        else:
            # select the rightmost display
            monitor = max(monitors, key=lambda m: m.x)

        # compute offset and center on that monitor
        offset_x, offset_y = monitor.x, monitor.y
        width, height = monitor.width, monitor.height
        center_x = offset_x + int((width - window_width) / 2)
        center_y = offset_y + int((height - window_height) / 2)

        # Positioning of the defined window
        window_name.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def set_app_dpi_awareness(self) -> None:
        """Configure the application to be DPI aware to avoid scaling issues"""
        try:
            # Windows-specific DPI awareness
            from ctypes import windll
            # Newer Windows versions
            windll.shcore.SetProcessDpiAwareness(1)  # Process is DPI aware
        except (ImportError, Exception) as e:
            # If all DPI awareness methods fail, log it but continue
            print(f"Could not set DPI awareness, scaling might be affected: {e}")
        
        # Automatisch an DPI des Systems anpassen
        scaling_factor = self.get_scaling_factor()
        self.main.tk.call('tk', 'scaling', scaling_factor)
        print(scaling_factor)
    
    def get_scaling_factor(self) -> float:
        """Determine appropriate scaling factor based on monitor resolution"""
        monitors = get_monitors()
        monitor = monitors[0]  # Default to primary monitor
        
        # Use the selected monitor if specified
        if self.monitor_idx is not None and 0 <= self.monitor_idx < len(monitors):
            monitor = monitors[self.monitor_idx]
        
        # Base scaling on resolution
        if monitor.width >= 3840:  # 4K
            return 2.5
        elif monitor.width >= 2560:  # 2K/1440p
            return 2
        elif monitor.width >= 1920:  # Full HD
            return 1.75
        else:
            return 1.5

    def create_widgets(self) -> None:
        """Creates the main GUI components."""
        # Frame for the bankoption
        bankFrame = ttk.LabelFrame(self.main, text="", labelanchor="nw")
        bankFrame.pack(fill="both", expand=False, padx=10, pady=5)

        ## Bank Option
        bankoption = ttk.Label(bankFrame, text="Bank:")
        bankoption.pack(padx=5, pady=5, side="left")



        # Frame for the csv paths
        csvPaths = ttk.LabelFrame(self.main, text="Dateipfade", labelanchor="nw")
        csvPaths.pack(fill="both", expand=False, padx=10, pady=5)

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

        ## Load the paths from the current preset
        self.preset_manager.get_paths()  # Load the paths from the current preset
        
        ## Save button
        btnSavePaths = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: self.preset_manager.set_paths(self.InputEntry.get(), self.OutputEntry.get()))
        btnSavePaths.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    



        # Frame for the Input categories
        inputFrame = ttk.LabelFrame(self.main, text="Einnahmen", labelanchor="n")
        inputFrame.pack(fill="both", expand=True, padx=10, pady=5)

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
        outputFrame.pack(fill="both", expand=True, padx=10, pady=5)

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
        saveFrame.pack(fill="both", expand=False, padx=10, pady=5)

        ## Save all Categories
        btnSaveCategories = ttk.Button(saveFrame, text="Speichere Kategorien", command=lambda: self.data_manager.save_all_treeviews(self.treeInput, self.treeOutput))
        btnSaveCategories.pack(padx=5, pady=5, side="top")



        # Frame for presets
        presetsFrame = ttk.LabelFrame(self.main, text="Presets", labelanchor="nw")
        presetsFrame.pack(fill="both", expand=True, padx=10, pady=5)
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



        # Keyboard shortcut bindings

        ## Bind the delete key to all treeviews
        self.main.bind_class("Treeview", "<Delete>", self.kb_tree_delete_row)


    def update_preset_menu(self) -> None:
        """Update the OptionMenu with the latest presets."""
        menu = self.presetMenu["menu"]
        menu.delete(0, "end")  # Clear the current options
        
        for preset in self.preset_manager.presets:
            # Use a lambda that calls on_preset_change with the preset name
            menu.add_command(label=preset, command=lambda value=preset: self.preset_manager.on_preset_change(value))       



    # Methods for Keyboard shortcuts

    def kb_tree_delete_row(self, event) -> None:
        """Handles the delete key event for treeviews."""
        if event.keysym == "Delete":
            # Check which treeview is focused and delete the selected item
            if self.main.focus_get() == self.treeInput:
                selected_rows = self.treeInput.selection()
                for row in selected_rows:
                    self.treeInput.delete(row)
            elif self.main.focus_get() == self.treeOutput:
                selected_rows = self.treeOutput.selection()
                for row in selected_rows:
                    self.treeOutput.delete(row)
