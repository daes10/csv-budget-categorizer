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
 
        self.set_app_dpi_awareness()

        # Calculate window size based on screen resolution
        window_width, window_height = self.calculate_window_size()
        self.center_window(window_width, window_height, self.app.main)

        self.app.main.resizable(True, True)

        # * DEBUGGING
        logger.debug(f"{self.__str__()}")

    def __str__(self) -> str:
        """"Returns a string representation of the WindowManager instance."""
        return f"WindowManager: \n  -> monitor_idx= {self.monitor_idx},\n  -> app= {self.app},\n  -> window_width= {self.calculate_window_size()[0]},\n  -> window_height= {self.calculate_window_size()[1]}"

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

    def set_app_dpi_awareness(self) -> None:
        """Configure the application to be DPI aware to avoid scaling issues"""
        try:
            # Windows-specific DPI awareness
            from ctypes import windll
            # Newer Windows versions
            windll.shcore.SetProcessDpiAwareness(1)  # Process is DPI aware
        except (ImportError, Exception) as e:
            # If all DPI awareness methods fail, log it but continue
            logger.error(f"Could not set DPI awareness, scaling might be affected: {e}")
        
        # Automatisch an DPI des Systems anpassen
        scaling_factor = self.get_scaling_factor()
        self.app.main.tk.call('tk', 'scaling', scaling_factor)
    
    def get_scaling_factor(self) -> float:
        """Determine appropriate scaling factor based on monitor resolution and DPI"""
        monitors = get_monitors()
        monitor = monitors[0]  # Default to primary monitor
        
        # Use the selected monitor if specified
        if self.monitor_idx is not None and 0 <= self.monitor_idx < len(monitors):
            monitor = monitors[self.monitor_idx]
        
        # Get DPI value from Windows if possible
        try:
            from ctypes import windll, c_int
            user32 = windll.user32
            dpi = user32.GetDpiForSystem()  # Gets the system DPI
             
            # Base scaling on both resolution and DPI
            if dpi >= 144:  # High DPI (150% or higher scaling)
                dpi_factor = 1.5
            elif dpi >= 120:  # Medium-high DPI (125% scaling)
                dpi_factor = 1.25
            elif dpi >= 96:  # Standard DPI (100% scaling)
                dpi_factor = 1.0
            else:
                dpi_factor = 0.9  # Lower than standard
                
            # Combine resolution and DPI factors
            if monitor.width >= 3840:  # 4K
                res_factor = 2.0
            elif monitor.width >= 2560:  # 2K/1440p
                res_factor = 1.75
            elif monitor.width >= 1920:  # Full HD
                res_factor = 1.5
            else:
                res_factor = 1.0

            # * DEBUGGING
            logger.debug(f"Resolution factor: {res_factor}\nDPI factor: {dpi_factor}\nMonitor (width x height): {monitor.width}x{monitor.height}")
            logger.debug(f"Scaling factor: {res_factor * dpi_factor}")
            # Combine both factors for a more accurate scaling
            return res_factor * dpi_factor
            
        except Exception as e:
            logger.error(f"Could not get DPI value: {e}. Falling back to resolution-based scaling.")
            
            # Fall back to original resolution-based scaling
            if monitor.width >= 3840:  # 4K
                return 2.75
            elif monitor.width >= 2560:  # 2K/1440p
                return 2.25
            elif monitor.width >= 1920:  # Full HD
                return 1.75
            else:
                return 1.0
            
    def calculate_window_size(self) -> tuple:
        """Calculate window size based on screen resolution."""
        monitors = get_monitors()
        if self.monitor_idx is not None and 0 <= self.monitor_idx < len(monitors):
            monitor = monitors[self.monitor_idx]
        else:
            monitor = max(monitors, key=lambda m: m.x)
        
        # Use percentage of screen size for window dimensions
        # Default to 75% of screen width and 80% of screen height
        width = int(monitor.width * 0.75)
        height = int(monitor.height * 0.80)
        
        # Set minimum and maximum sizes to ensure usability
        width = max(800, min(width, 1920))  # Min 800px, Max 1920px
        height = max(600, min(height, 1200))  # Min 600px, Max 1200px
        
        # * DEBUGGING
        logger.debug(f"Calculated App Window size: {width}x{height}")

        return width, height
