import tkinter as tk
#print("Hallo es hat geklappt!")

# Erstelle ein neues Fenster (main)
main = tk.Tk()


# place a label on the main window
message = tk.Label(main, text="Hello, World!")
message.pack()

main.mainloop()

