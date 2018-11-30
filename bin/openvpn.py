from bin.credentials import *
from bin.root import *
from bin.root import askRootPassword
import logging

OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp"]
MAXIMUM_TRIES = 5

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class LoginError(Exception):
    pass


def get_path_to_conf(server, protocol):
    return CURRENT_PATH + "ovpn_" + PROTOCOLS[protocol] + "/" + server + "." + PROTOCOLS[protocol] + OVA_SUFFIX


def startVPN(server, protocol, sudoPassword):

    # obtains root access
    if sudoPassword is None:
        tmp = askRootPassword()

        if tmp is None:
            return None

        sudoPassword = tmp

    getRootPermissions(sudoPassword)

    print("Obtained root access")

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

    return openvpn, sudoPassword


def checkOpenVPN():
    c = subprocess.Popen(["ps ax | grep openvpn | grep -v grep"], stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, _) = c.communicate()
    if out != '':
        return True
    return False
