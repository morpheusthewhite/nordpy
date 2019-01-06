import os


def calculatePath(pathToModule):
    """
    Calculate the path to the current folder
    :param pathToModule: the path to the a module in a subdirectory
    :return: a string indicating the path
    """
    pathElements = pathToModule.split("/")

    result='/'

    for i, elem in enumerate(pathElements):
        if i < len(pathElements)-2:
            result = os.path.join(result, elem)

    return os.path.join("")


CURRENT_PATH = calculatePath(os.path.realpath(__file__))
