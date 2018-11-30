from bin.pathUtil import CURRENT_PATH
from bin.networkSelection import PROTOCOLS
import os

SETTING_FILENAME = "settings.ini"
SETTING_FILE = CURRENT_PATH + SETTING_FILENAME

# Comment inserted in settings.ini
COMMENT_STRING='# This is the configuration file for nordpy. Please do not change it manually'

def correct_saved_settings():

    with open(SETTING_FILE) as setting_file:

        protocol = setting_file.readline().strip()
        if(protocol not in PROTOCOLS):
            return False

        mode = setting_file.readline().strip()
        if(mode not in ['0', '1']):
            return False

    return True

def exists_saved_settings():
    # checking if config file exists and is correctly saved
    if(not os.path.exists(SETTING_FILE) or not correct_saved_settings()):
        return False


def update_settings(serverType, protocol):
    with open(SETTING_FILE, "w") as f:
        print(COMMENT_STRING)
        print(serverType, file=f)
        print(protocol, file=f)
    return


def load_settings():
    with open(SETTING_FILE, "r") as f:
        f.readline().strip() # removing comment

        serverType = f.readline().strip()
        protocol = f.readline().strip()

    return serverType, protocol