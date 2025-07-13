# --- utils/logger.py ---
import logging
import os
from datetime import datetime

def setup_logger() -> logging.Logger:
    """Sets up the logger with a file handler and a stream handler.
    Creates a logs directory if it doesn't exist.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"task_manager_{timestamp}.log")

    logger = logging.getLogger("TaskManagerLogger")
    logger.setLevel(logging.DEBUG)  # Set the overall logger level

    # File Handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG) # Log everything to the file
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Stream Handler (Console)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Log only INFO and above to the console
    stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    return logger

logger = setup_logger()

