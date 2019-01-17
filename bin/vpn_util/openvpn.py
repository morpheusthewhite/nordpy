from bin.credentials import *
from bin.root import *
from bin.logging_util import get_logger
from bin.vpn_util.exceptions import LoginError

OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp", "Ikev2/IPsec"]
MAXIMUM_TRIES = 2
IKEV2_PROTOCOL_NUMBER = 2

logger = get_logger(__name__)


def get_path_to_conf(server, protocol):
    """
    calculates the path to the .ovpn file from the given server and protocol
    :param server: the name of the server
    :param protocol: the protocol to be used
    :return: the path to the file
    """
    return CURRENT_PATH + "ovpn_" + PROTOCOLS[protocol] + "/" + server + "." + PROTOCOLS[protocol] + OVA_SUFFIX


def start_openvpn(server, protocol):
    pathToConf = get_path_to_conf(server, protocol)
    args = ["sudo", "openvpn", "--config", pathToConf, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME]

    tries = 0
    while tries < MAXIMUM_TRIES:

        openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)

        while True:
            line = openvpn.stdout.readline()

            if not line.strip() == '':
                logger.debug("[OPENVPN]: "+line)

            if "Initialization Sequence Completed" in line:
                # success !
                return openvpn
            elif "connection failed" in line or "Exiting" in line:
                tries += 1
                openvpn.terminate()
                break

            elif "AUTH_FAILED" in line:
                # something's wrong
                raise LoginError

    raise ConnectionError

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
