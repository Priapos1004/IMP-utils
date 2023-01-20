import logging
import sys


def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    c_handler = logging.StreamHandler(sys.stdout)

    c_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    c_handler.setFormatter(c_format)

    # to prevent double logging output
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.propagate = False

    logger.addHandler(c_handler)
    return logger
