from bin.pathUtil import CURRENT_PATH
from bin.networkSelection import MODES
from bin.openvpn import get_path_to_conf
import os
import configparser as cp
import logging

SETTING_FILENAME = "settings.ini"
SETTING_FILE = CURRENT_PATH + SETTING_FILENAME

# Comment inserted in settings.ini
COMMENT_STRING = 'This is the configuration file for nordpy. Please do not change it manually'
DEFAULT_SETTING = 'DEFAULT'
SERVER_TYPE_KEY = 'Server Type'
PROTOCOL_KEY = 'Protocol'
LAST_CONNECTED_KEY = 'Last Connected Server'

configparser = cp.ConfigParser()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def is_not_valid_server(server_string, protocol):
    conf_filename = get_path_to_conf(server_string, protocol)

    return os.path.exists(conf_filename)


def correct_saved_settings():
    mode, protocol, recommended_server = load_settings()
    logger.debug("Verifing saved file")

    if mode not in MODES:
        logger.debug(SERVER_TYPE_KEY + " not correct")
        return False

    if protocol not in ['0', '1']:
        logger.debug(PROTOCOL_KEY + " not correct")
        return False

    if is_not_valid_server(recommended_server, int(protocol)):
        logger.debug(LAST_CONNECTED_KEY + " not correct")
        return False

    logger.debug("File is correct")
    return True


def exists_saved_settings():
    # checking if config file exists and is correctly saved
    if not os.path.exists(SETTING_FILE) or not correct_saved_settings():
        return False


def update_settings(serverType, protocol, recommended_server):
    configparser[DEFAULT_SETTING] = {SERVER_TYPE_KEY: serverType,
                                     PROTOCOL_KEY: protocol, LAST_CONNECTED_KEY: recommended_server}

    logger.debug("Updating setting file")
    with open(SETTING_FILE, "w") as settings_file:
        # configparser[DEFAULT_SETTING]["; " + COMMENT_STRING] = None
        configparser.write(settings_file)
    return


def load_settings():
    with open(SETTING_FILE, "r") as settings_file:
        configparser.read(settings_file)

    try:
        return configparser[DEFAULT_SETTING][SERVER_TYPE_KEY], configparser[DEFAULT_SETTING][PROTOCOL_KEY],\
        configparser[DEFAULT_SETTING][LAST_CONNECTED_KEY]
    except KeyError:
        return None, None, None