from bin.pathUtil import CURRENT_PATH
import os

SETTING_FILENAME = "settings.ini"
SETTING_FILE = CURRENT_PATH + SETTING_FILENAME


def exists_saved_settings():
    return os.path.exists(SETTING_FILE)


def update_settings(serverType, protocol):
    with open(SETTING_FILE, "w") as f:
        print(serverType, file=f)
        print(protocol, file=f)
    return


def load_settings():
    with open(SETTING_FILE, "r") as f:
        serverType = f.readline().strip()
        protocol = f.readline().strip()

    return serverType, protocol