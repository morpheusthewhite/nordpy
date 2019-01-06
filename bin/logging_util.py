import logging

GLOBAL_LOGGING_LEVEL = logging.DEBUG


def get_logger(name):
    """
    Creates a logger with the passed name
    :param name: usually the name of the module which invokes this function
    :return: the logger
    """
    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(GLOBAL_LOGGING_LEVEL)

    return logger