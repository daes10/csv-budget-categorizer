import tkinter as tk
from tkinter import ttk # import themed tk
#print("Hallo es hat geklappt!")

# create a main window
main = tk.Tk()
main.title("CSV Formatter")

# Geometry of the main window
main_width = 1000
main_height = 600

# Get the screen dimension
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - main_width / 2)
center_y = int(screen_height/2 - main_height / 2)

# set the position of the window to the center of the screen
main.geometry(f'{main_width}x{main_height}+{center_x}+{center_y}')

# set the icon of the main window
main.iconbitmap('./img/format_icon.ico')

main.title("CSV Formatter")

# create a function that will be called when the button is clicked
def button_clicked():
    print("Button clicked!")

# frame for the bank
bankFrame = ttk.LabelFrame(main, text="Bankselektion", labelanchor="n")
bankFrame.pack(fill="both", expand="no", padx=10, pady=5)

bankoption = ttk.Label(bankFrame, text="Bank:")
bankoption.pack(padx=5, pady=5, side="left")

# frame for the csv paths
csvPaths = ttk.LabelFrame(main, text="Dateipfade", labelanchor="n")
csvPaths.pack(fill="both", expand="yes", padx=10, pady=5)

# input path label and entry
InputLabel = ttk.Label(csvPaths, text="CSV-Einlesedatei:")
InputLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
InputEntry = ttk.Entry(csvPaths)
InputEntry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
csvPaths.columnconfigure(1, weight=1)
# output path label and entry
OutputLabel = ttk.Label(csvPaths, text="CSV-Ausgabepfad:")
OutputLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
OutputEntry = ttk.Entry(csvPaths)
OutputEntry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
csvPaths.columnconfigure(1, weight=1)

# frame for the input categories
inputcategories = ttk.LabelFrame(main, text="Einnahmen", labelanchor="n")
inputcategories.pack(fill="both", expand="yes", padx=10, pady=5)

# frame for the output categories
outputcategories = ttk.LabelFrame(main, text="Ausgaben", labelanchor="n")
outputcategories.pack(fill="both", expand="yes", padx=10, pady=5)


# button = ttk.Button(main, text="Click me", command=button_clicked).pack()

# place a label on the main window
# tk.Label(main, text="Hello, World!").pack()


main.mainloop()

