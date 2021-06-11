import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger(__name__)

    # remove duplicate handlers created from run_logger() in multiple files.
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = RotatingFileHandler('../logs/grad_ts.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger
