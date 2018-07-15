from bin.credentials import *
from bin.root import *
PATH_TO_OPENVPN = "/etc/openvpn/ovpn_"
OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp"]

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

    openvpn = subprocess.Popen(args, stdin=subprocess.PIPE, universal_newlines=True)

    return openvpn, sudoPassword

