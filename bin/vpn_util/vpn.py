from bin.vpn_util.ikev2 import ikev2_connect, ikev2_is_running
from bin.vpn_util.openvpn import *


def startVPN(server, protocol):
    """
    Starts VPN with the given server and protocol. Raises a ConnectionError if no connection is available
    and a LoginError if the credentials are wrong
    :param server: the name of the server
    :param protocol: the protocol to be used
    :return: a Popen object if a openvpn started successfully, None if it is an ikev2
    """
    if not check_credentials():
        try:
            save_credentials()
        except NoCredentialsProvidedException:
            return None

    if protocol == IKEV2_CODE:  # if it is ikev2/ipvsec
        username, password = read_saved_credentials()
        ikev2_connect(username, password, server)
    else:
        start_openvpn(server, protocol)


def is_vpn_running():
    """
    checks if some type of VPN connection is already running
    :return: True if is running, False otherwise
    """
    return checkOpenVPN()
