from bin.pathUtil import CURRENT_PATH
from bin.vpn_util.networkSelection import MODES
from bin.vpn_util.openvpn import get_path_to_conf
import os
import configparser as cp
from bin.logging_util import get_logger
from bin.vpn_util.networkSelection import COUNTRY_CODES, AUTOMATIC_CHOICE_STRING

SETTING_FILENAME = "settings.ini"
SETTING_FILE = CURRENT_PATH + SETTING_FILENAME

# Comment inserted in settings.ini
COMMENT_STRING = 'This is the configuration file for nordpy. Please do not change it manually'
DEFAULT_SETTING = 'DEFAULT'
SERVER_TYPE_KEY = 'Server Type'
PROTOCOL_KEY = 'Protocol'
LAST_CONNECTED_KEY = 'Last Connected Server'
LAST_COUNTRY_KEY = 'Last country'

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
    saved_settings = load_settings()
    if saved_settings is None:
        return False

    mode, protocol, country, recommended_server = saved_settings
    logger.debug("Verifing saved file")

    if mode not in MODES:
        logger.info(SERVER_TYPE_KEY + " not correct")
        logger.debug(mode)
        return False

    if int(protocol) not in range(0, 3):
        logger.info(PROTOCOL_KEY + " not correct")
        logger.debug(protocol)
        return False

    if country not in COUNTRY_CODES.keys() and not country == AUTOMATIC_CHOICE_STRING:
        logger.info(LAST_COUNTRY_KEY + " not correct")
        logger.debug(country)
        return False

    if is_not_valid_server(recommended_server, 0):  # protocol does not matter
        logger.info(LAST_CONNECTED_KEY + " not correct")
        logger.debug(recommended_server)
        return False

    logger.debug("File is correct")
    return True


def existing_corrected_saved_settings():
    """
    checks if config file exists and is correctly saved
    :return: True if is saved and correct, False otherwise
    """
    if not os.path.exists(SETTING_FILE) or not correct_saved_settings():
        return False

    return True


def update_settings(server_type, protocol, country, recommended_server):
    """
    Updates the saved settings
    :param server_type: the type of the server used
    :param protocol: the protocol used
    :param country: the country selected
    :param recommended_server: the recommended server
    """

    configparser[DEFAULT_SETTING] = {SERVER_TYPE_KEY: server_type,
                                     PROTOCOL_KEY: protocol,
                                     LAST_COUNTRY_KEY: country,
                                     LAST_CONNECTED_KEY: recommended_server}

    logger.debug("Updating setting file")
    with open(SETTING_FILE, "w") as settings_file:
        # configparser[DEFAULT_SETTING]["; " + COMMENT_STRING] = None
        configparser.write(settings_file)


def load_settings():
    """
    Reads the saved configurations
    :return: the read server type, the protocol, the country and the last recommended server or None
    if some error were faced during the read (for example the saved file is incorrect)
    """
    configparser.read(SETTING_FILE)

    try:
        return configparser[DEFAULT_SETTING][SERVER_TYPE_KEY], \
               configparser[DEFAULT_SETTING][PROTOCOL_KEY],\
               configparser[DEFAULT_SETTING][LAST_COUNTRY_KEY],\
               configparser[DEFAULT_SETTING][LAST_CONNECTED_KEY]
    except KeyError:
        logger.debug("Key not found")
        return None


ADV_SETTINGS = 'OTHER'
FACTOR_SCALE_KEY = 'Factor Scale'


def advanced_settings_save(factor_scale):
    """
    Saves advanced settings
    :param factor_scale: the scale factor for the dimensions of the main window
    """
    configparser[ADV_SETTINGS] = {FACTOR_SCALE_KEY: str(factor_scale)}
    logger.debug('Saved '+str(factor_scale))

    logger.debug("Updating advanced setting file")
    with open(SETTING_FILE, "w") as settings_file:
        configparser.write(settings_file)


def advanced_settings_read():
    """
    Reads advanced settings
    :return: the factor scale, None if a key was not found
    """
    try:
        print(SETTING_FILE)
        configparser.read(SETTING_FILE)
        scale_factor = int(configparser[ADV_SETTINGS][FACTOR_SCALE_KEY])
        logger.debug("Read a factor scale of "+str(scale_factor))
        return scale_factor
    except KeyError:
        logger.debug("Key not found")
        return None

def advanced_settings_are_correct():
    """
    Checks if advanced settings are saved correctly
    :return: True if is correct, false otherwise
    """
    try:
        configparser.read(SETTING_FILE)
        scale_factor = int(configparser[ADV_SETTINGS][FACTOR_SCALE_KEY])
        return scale_factor <= 3 and scale_factor >= 0.5
    except (KeyError, ValueError):
        return False