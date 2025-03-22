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


button = ttk.Button(main, text="Click me", command=button_clicked).pack()

# place a label on the main window
tk.Label(main, text="Hello, World!").pack()


main.mainloop()

