
# --- utils/config.py ---
import json
import os
from dotenv import load_dotenv
# import logging
from .logger import setup_logger
logger = setup_logger()
# # Create and configure the logger
# logger = logging.getLogger(__name__) 

def load_config(config_file: str = "config.json") -> dict:
    """Loads configuration from a JSON file and environment variables.

    Args:
        config_file: The path to the configuration file.

    Returns:
        A dictionary containing the configuration.
    """
    config = {}
    # Load from JSON file
    try:
        with open(config_file, "r") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        logger.warning(f"Configuration file '{config_file}' not found.")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON in '{config_file}'.")
    except Exception as e:
         logger.exception(f"Error reading config file: {e}")


    # Load from .env file, overriding JSON values
    load_dotenv()
    for key, value in os.environ.items():
        config[key] = value

    return config

config = load_config()
