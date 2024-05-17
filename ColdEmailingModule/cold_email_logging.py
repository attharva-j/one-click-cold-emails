import logging
import sys

def get_logger():
    # Create a custom logger
    logger = logging.getLogger('send_cold_emails')
    logger.setLevel(logging.INFO)  # Set the level for the custom logger

    # Create handlers
    file_handler = logging.FileHandler('cold_email_logs.log')
    stdout_handler = logging.StreamHandler(sys.stdout)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    return logger