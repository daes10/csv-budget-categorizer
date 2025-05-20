# system imports
import argparse
import tkinter as tk
import customtkinter as ctk

# local imports
from .gui import App

def main():
    """Entry point for the CSV Formatter application."""
    # Parse optional monitor argument
    parser = argparse.ArgumentParser(description="CSV Formatter Application")
    parser.add_argument("--monitor", type=int, default=None,
                        help="Index of monitor to launch window on (0-based, default: rightmost)")
    args = parser.parse_args()
    
    # Launch app on desired monitor
    app = App(monitor_idx=args.monitor)
    app.main.mainloop()

if __name__ == "__main__":
    main()