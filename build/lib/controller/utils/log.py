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
    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(logging.INFO)  # Console handler handles from INFO level

    file_handler_info = logging.FileHandler('logs/info.log')
    file_handler_info.setLevel(logging.INFO)  # File handler for info handles from INFO level

    file_handler_error = logging.FileHandler('logs/error.log')
    file_handler_error.setLevel(logging.ERROR)  # File handler for error handles from ERROR level

    file_handler_debug = logging.FileHandler('logs/debug.log')
    file_handler_debug.setLevel(logging.DEBUG)  # File handler for debug handles from DEBUG level

    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    terminal_handler.setFormatter(log_format)
    file_handler_info.setFormatter(log_format)
    file_handler_error.setFormatter(log_format)
    file_handler_debug.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(terminal_handler)
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_error)
    logger.addHandler(file_handler_debug)