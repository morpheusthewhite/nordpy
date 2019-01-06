from bin.credentials import *
from bin.root import *
from bin.root import ask_root_password
from bin.logging_util import get_logger

OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp"]
MAXIMUM_TRIES = 5

logger = get_logger(__name__)


class LoginError(Exception):
    pass


def get_path_to_conf(server, protocol):
    """
    calculates the path to the .ovpn file from the given server and protocol
    :param server: the name of the server
    :param protocol: the protocol to be used
    :return: the path to the file
    """
    return CURRENT_PATH + "ovpn_" + PROTOCOLS[protocol] + "/" + server + "." + PROTOCOLS[protocol] + OVA_SUFFIX


def startVPN(server, protocol, sudoPassword):
    """
    Launches openvpn with the given server and protocol. Raises a ConnectionError if no connection is available
    :param server: the name of the server
    :param protocol: the protocol to be used
    :param sudoPassword: the root password
    :return: a Popen object
    """
    get_root_permissions(sudoPassword)

    if not check_credentials():
        try:
            save_credentials()
        except NoCredentialsProvidedException:
            return None

    pathToConf = get_path_to_conf(server, protocol)
    args = ["sudo", "openvpn", "--config", pathToConf, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME]

    openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)

    tries=0

    while True:
        line = openvpn.stdout.readline()

        if not line.strip() == '':
            logger.debug("[OPENVPN]: "+line)

        if "Initialization Sequence Completed" in line:
            break
        elif "connection failed" in line:
            if tries < MAXIMUM_TRIES:
                tries += 1
            else:
                openvpn.terminate()
                raise ConnectionError
        elif "AUTH_FAILED" in line:
            raise LoginError

    return openvpn


def checkOpenVPN():
    """
    Checks if a openvpn process is already running
    :return: True if is running, False otherwise
    """
    c = subprocess.Popen(["ps ax | grep openvpn | grep -v grep"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, _) = c.communicate()
    if out != '':
        return True
    return False
