# system imports
import logging
import os


def setup_logger():
    """Configure and return a logger instance for the application."""
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = f"{log_dir}/logging.log"

    # Configure logging
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
        datefmt = "%m.%d.%Y %I:%M:%S",
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also output to console
        ]
    )

    return logging.getLogger("default_logger")

# Create a shared logger instance
logger = setup_logger()
