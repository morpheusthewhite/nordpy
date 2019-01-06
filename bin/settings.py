from bin.pathUtil import CURRENT_PATH
from bin.networkSelection import MODES
from bin.openvpn import get_path_to_conf
import os
import configparser as cp
from bin.logging_util import get_logger

SETTING_FILENAME = "settings.ini"
SETTING_FILE = CURRENT_PATH + SETTING_FILENAME

# Comment inserted in settings.ini
COMMENT_STRING = 'This is the configuration file for nordpy. Please do not change it manually'
DEFAULT_SETTING = 'DEFAULT'
SERVER_TYPE_KEY = 'Server Type'
PROTOCOL_KEY = 'Protocol'
LAST_CONNECTED_KEY = 'Last Connected Server'

configparser = cp.ConfigParser()
logger = get_logger(__name__)


def is_not_valid_server(server_string, protocol):
    """
    Checks if the given server and protocol correspond to an existing server
    :param server_string: the name of the server
    :param protocol: the protocol to be used
    :return: True if it exists, False otherwise
    """
    conf_filename = get_path_to_conf(server_string, protocol)

    return not os.path.exists(conf_filename)


def correct_saved_settings():
    """
    Check if the saved settings are correct
    :return: True if they are correct, False otherwise
    """
    mode, protocol, recommended_server = load_settings()
    logger.debug("Verifing saved file")

    if mode not in MODES:
        logger.debug(SERVER_TYPE_KEY + " not correct")
        logger.debug(mode)
        return False

    if protocol not in ['0', '1']:
        logger.debug(PROTOCOL_KEY + " not correct")
        logger.debug(protocol)
        return False

    if is_not_valid_server(recommended_server, int(protocol)):
        logger.debug(recommended_server)
        logger.debug(LAST_CONNECTED_KEY + " not correct")
        return False

    logger.debug("File is correct")
    return True


def exists_saved_settings():
    """
    checks if config file exists and is correctly saved
    :return: True if is saved and correct, False otherwise
    """
    if not os.path.exists(SETTING_FILE) or not correct_saved_settings():
        return False


def update_settings(serverType, protocol, recommended_server):
    """
    Updates the saved settings
    :param serverType: the type of the server used
    :param protocol: the protocol used
    :param recommended_server: the recommended server
    """
    configparser[DEFAULT_SETTING] = {SERVER_TYPE_KEY: serverType,
                                     PROTOCOL_KEY: protocol, LAST_CONNECTED_KEY: recommended_server}

    logger.debug("Updating setting file")
    with open(SETTING_FILE, "w") as settings_file:
        # configparser[DEFAULT_SETTING]["; " + COMMENT_STRING] = None
        configparser.write(settings_file)


def load_settings():
    """
    Reads the saved configurations
    :return: the read server type, the protocol and the last recommended server or (None, None, None)
    if some error were faced during the read (for example the saved file is incorrect)
    """
    configparser.read(SETTING_FILE)

    try:
        return configparser[DEFAULT_SETTING][SERVER_TYPE_KEY], \
               configparser[DEFAULT_SETTING][PROTOCOL_KEY],\
               configparser[DEFAULT_SETTING][LAST_CONNECTED_KEY]
    except KeyError:
        logger.debug("Key not found")
        return None, None, None