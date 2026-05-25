import logging
from datetime import datetime
from pathlib import Path

def get_next_log_filename(base_name="app_errors", extension=".txt", directory="."):
    """
    Finds the next available incremented filename.
    Example: app_errors_1.txt, app_errors_2.txt, etc.
    """
    dir_path = Path(directory)
    counter = 1

    while True:
        filename = f"{base_name}_{counter}{extension}"
        file_path = dir_path / filename

        if not file_path.exists():
            return str(file_path)

        counter += 1

def configure_logger(base_name="app_errors", directory="data/logs"):
    """
    Sets up the logger with a dynamically incremented file name.
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

    log_filename = get_next_log_filename(
        base_name=base_name,
        extension=".txt",
        directory=directory
    )

    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )

    print(f"Logging initialized. Writing to: {log_filename}")

def log_error(exception: str, context_msg: str):
    "Logs error w/ custom error msg w/ date"
    exception_msg = str(exception)
    full_message = f"{context_msg} -> Details: {exception_msg}"
    logging.error(full_message)