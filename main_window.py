import tkinter as tk
from tkinter import ttk # import themed tk

#imports of my own modules
import functions as fnct
from functions import *

# create a main window
main = tk.Tk()
main.title("CSV Formatter")


# set the icon of the main window
main.iconbitmap('./img/format_icon.ico')

main.title("CSV Formatter")

# set the position of the window to the center of the screen
fnct.center_screen(1000, 600, main)





# frame for the bank
bankFrame = ttk.LabelFrame(main, text="Bankselektion", labelanchor="n")
bankFrame.pack(fill="both", expand="no", padx=10, pady=5)

bankoption = ttk.Label(bankFrame, text="Bank:")
bankoption.pack(padx=5, pady=5, side="left")

# frame for the csv paths
csvPaths = ttk.LabelFrame(main, text="Dateipfade", labelanchor="n")
csvPaths.pack(fill="both", expand="no", padx=10, pady=5)

# input path
InputLabel = ttk.Label(csvPaths, text="CSV-Einlesedatei:")
InputLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
InputEntry = ttk.Entry(csvPaths)
InputEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
csvPaths.columnconfigure(1, weight=1)
btnFileInput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: select_filepath(InputEntry))
btnFileInput.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

# output path
OutputLabel = ttk.Label(csvPaths, text="CSV-Ausgabepfad:")
OutputLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
OutputEntry = ttk.Entry(csvPaths)
OutputEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
csvPaths.columnconfigure(1, weight=1)
btnFileOutput = ttk.Button(csvPaths, text="Datei auswählen", command=lambda: select_filepath(OutputEntry))
btnFileOutput.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# load paths from settings.json if it exists
fnct.load_paths_to_entry(InputEntry, OutputEntry)

# save button
saveBtn = ttk.Button(csvPaths, text="Speichert Pfade", command=lambda: fnct.save_paths(InputEntry.get(), OutputEntry.get()))
saveBtn.grid(row=2, column=2, padx=5, pady=5, sticky="ew")


# frame for the input categories
inputFrame = ttk.LabelFrame(main, text="Einnahmen", labelanchor="n")
inputFrame.pack(fill="both", expand="yes", padx=10, pady=5)

# Create the Treeview widget
treeInput = ttk.Treeview(inputFrame, columns=("category", "filters", "dateFrom", "dateTo", "minValue", "maxValue"), show="headings")
treeInput.heading("category", text="Kategorie")
treeInput.heading("filters", text="Suchbegriff")
treeInput.heading("dateFrom", text="Datum von")
treeInput.heading("dateTo", text="Datum bis")
treeInput.heading("minValue", text="Min. Betrag")
treeInput.heading("maxValue", text="Max. Betrag")
treeInput.pack(fill="both", expand="yes", padx=10, pady=5)

# Configure the columns in the Treeview widget
for col in treeInput["columns"]:
    treeInput.column(col, width=100, stretch=True, anchor="center")

# treeInput.insert()






# frame for the output categories
outputFrame = ttk.LabelFrame(main, text="Ausgaben", labelanchor="n")
outputFrame.pack(fill="both", expand="yes", padx=10, pady=5)


# button = ttk.Button(main, text="Click me", command=button_clicked).pack()

# place a label on the main window
# tk.Label(main, text="Hello, World!").pack()



main.mainloop()

