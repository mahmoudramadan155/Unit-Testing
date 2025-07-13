
# --- utils/config.py ---
import json
import os
from dotenv import load_dotenv
from .logger import setup_logger

logger = setup_logger()

def load_config(config_file: str = "config.json") -> dict:
    """Loads configuration from JSON and .env files."""
    config = {}
    try:
        with open(config_file, "r") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        logger.warning(f"Configuration file '{config_file}' not found.")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON in '{config_file}'.")

    load_dotenv()
    config.update(os.environ)  # .env overrides JSON
    return config

config = load_config()
