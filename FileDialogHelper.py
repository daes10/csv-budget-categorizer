# FileDialogHelper
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class FileDialogHelper:
    """A helper class for file dialog operations"""
    def __init__(self):
        pass
    
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