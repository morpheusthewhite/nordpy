import logging

GLOBAL_LOGGING_LEVEL = logging.DEBUG

def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(GLOBAL_LOGGING_LEVEL)

    return logger