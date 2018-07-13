import os


def calculatePath(pathToModule):
    pathElements = pathToModule.split("/")

    result='/'

    for i, elem in enumerate(pathElements):
        if i < len(pathElements)-2:
            result = os.path.join(result, elem)

    return result+"/"


CURRENT_PATH = calculatePath(os.path.realpath(__file__))
