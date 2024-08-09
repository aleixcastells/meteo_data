# logger.py

import os
import logging
from helpers.time import get_timestamp_today

logging_directory = "./logs"
if not os.path.exists(logging_directory):
    os.makedirs(logging_directory)


log_file = os.path.join(logging_directory, f"meteo_log_{get_timestamp_today()}.log")

# Configure the logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # Set the minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log(level, message):
    level = level.lower()
    if level == "debug":
        logging.debug(message)
    elif level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    elif level == "critical":
        logging.critical(message)
    else:
        logging.error(f"Invalid log level: {level}. Message: {message}")

    print(f"[{level}] {message}")
