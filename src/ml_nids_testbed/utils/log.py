import logging
import os

def setup_logging():
    # Create a logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set to lowest level

    # Create handlers
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)  # Console handler handles from INFO level

    f_handler_info = logging.FileHandler('logs/info.log')
    f_handler_info.setLevel(logging.INFO)  # File handler for info handles from INFO level

    f_handler_error = logging.FileHandler('logs/error.log')
    f_handler_error.setLevel(logging.ERROR)  # File handler for error handles from ERROR level

    # Create formatters and add it to handlers
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(format)
    f_handler_info.setFormatter(format)
    f_handler_error.setFormatter(format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler_info)
    logger.addHandler(f_handler_error)