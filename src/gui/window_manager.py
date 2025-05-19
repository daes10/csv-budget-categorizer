# system imports
import tkinter as tk
from screeninfo import get_monitors 
import customtkinter as ctk

# local imports
from ..utils.logging import logger

class WindowManager:
    """""Handles the window size and DPI awareness for the application."""
    def __init__(self, app, monitor_idx) -> None:
        self.app = app
        self.monitor_idx = monitor_idx
        
        # Set CustomTkinter appearance mode and default color theme
        ctk.set_appearance_mode("Light")  # "System" (follows OS), "Dark" or "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
 
        window_width, window_height = 1000, 850
        self.center_window(window_width, window_height, self.app.main)

        self.app.main.resizable(True, True)

        # * DEBUGGING
        logger.debug(f"{self.__str__()}")

    def __str__(self) -> str:
        """"Returns a string representation of the WindowManager instance."""
        return f"WindowManager: \n  -> monitor_idx= {self.monitor_idx},\n  -> app= {self.app}"

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
        window_name.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # Use self.app.main instead of window_name
