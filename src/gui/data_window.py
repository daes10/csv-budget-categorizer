# system imports
import tkinter as tk
import customtkinter as ctk

# local imports
from .window_manager import WindowManager
from ..utils.logging import logger

class DataWindow(ctk.CTkToplevel):
    def __init__ (self, main, app) -> None:
        super().__init__(main) # Initialize the parent class (CTkToplevel)
        self.app = app
        self.main = main

        self.title("Data Details")

        window_width, window_height = 400, 300
        self.app.window_manager.center_window(window_width, window_height, self)

        logger.debug("Data window initialized...")

        # * DEBUGGING
        logger.debug(f"{self.__str__()}")

    def __str__(self) -> str:
        """"Returns a string representation of the WindowManager instance."""
        return f"DataWindow: \n  -> app= {self.app},\n  -> main= {self.main}"

    def show(self):
        """Show the data window."""
        self.deiconify()
 