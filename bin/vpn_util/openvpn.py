from bin.credentials import *
from bin.root import *
from bin.logging_util import get_logger
from bin.vpn_util.exceptions import LoginError, OpenresolvError

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
    """
    starts openvpn connection with a certain protocol to a specific server. Raise a ConnectionError
    if the connection failed, a LoginError if the credentials are wrong or a OpenresolvError if openresolv is missing
    :param server: the server to which the connection will be established
    :param protocol: the protocol to be used (an integer)
    """
    pathToConf = get_path_to_conf(server, protocol)
    args = ["sudo", "openvpn", "--config", pathToConf, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME,
            # to prevent dns leaks
            "--script-security", "2", "--up", "/etc/openvpn/update-resolv-conf", "--down",
            "/etc/openvpn/update-resolv-conf"]

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

            # openresolv is not installed
            elif "script fails with" in line:
                raise OpenresolvError

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
