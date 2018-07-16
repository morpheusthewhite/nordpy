from bin.credentials import *
from bin.root import *


PATH_TO_OPENVPN = "/etc/openvpn/ovpn_"
OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp"]
MAXIMUM_TRIES = 5


class LoginError(Exception):
    pass


def startVPN(server, protocol, sudoPassword):

    # obtains root access
    if sudoPassword is None:
        sudoPassword = askRootPassword()
    getRootPermissions(sudoPassword)

    print("Obtained root access")

    if not check_credentials():
        save_credentials()

    pathToConf = PATH_TO_OPENVPN + PROTOCOLS[protocol] + "/" + server + "." + PROTOCOLS[protocol] + OVA_SUFFIX
    args = ["sudo", "openvpn", "--config", pathToConf, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME]

    openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)

    tries=0

    while True:
        line = openvpn.stdout.readline()
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
