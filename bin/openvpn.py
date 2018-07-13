from bin.credentials import *
from bin.root import *
PATH_TO_OPENVPN = "/etc/openvpn/ovpn_tcp/"
OVA_SUFFIX = ".tcp.ovpn"

def startVPN(server, sudoPassword):

    # obtains root access
    if sudoPassword is None:
        sudoPassword = askRootPassword()
    getRootPermissions(sudoPassword)

    print("Obtained root access")

    if not check_credentials():
        save_credentials()

    args = ["sudo", "openvpn", "--config", PATH_TO_OPENVPN + server + OVA_SUFFIX, "--auth-user-pass", CURRENT_PATH + CREDENTIALS_FILENAME]

    openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True)

    return openvpn, sudoPassword

