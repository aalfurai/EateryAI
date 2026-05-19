import logging
from datetime import datetime

def configure_logger(log_filename="app_errors.txt"):
    """Configure once at start of script."""
    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def log_error(exception, context_msg):
    "Logs error w/ custom error msg w/ date"
    full_message = f"{context_msg} -> Details: {str(exception)}"
    logging.error(full_message)