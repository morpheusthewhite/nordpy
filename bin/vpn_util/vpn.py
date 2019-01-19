from bin.vpn_util.ikev2 import ikev2_connect, ikev2_is_running, ikev2_disconnect, ipsec_exists
from bin.vpn_util.openvpn import *
IPSEC_EXISTS = ipsec_exists()


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

    if protocol == IKEV2_PROTOCOL_NUMBER:  # if it is ikev2/ipvsec
        username, password = read_saved_credentials()
        ikev2_connect(username, password, server)
    else:
        start_openvpn(server, protocol)


def stop_vpn(running_connection):
    if running_connection == OPENVPN_CONNECTION_STRING:
        subprocess.call(["sudo", "killall", "openvpn"])
    elif running_connection == IPSEC_CONNECTION_STRING:
        ikev2_disconnect()

    return

OPENVPN_CONNECTION_STRING = 'UDP/TCP'
IPSEC_CONNECTION_STRING = 'Ikev2'


def get_running_vpn():
    """
    checks if some type of VPN connection is already running
    :return: a string representing what is running, None otherwise
    """
    if checkOpenVPN():
        return OPENVPN_CONNECTION_STRING
    elif ikev2_is_running():
        return IPSEC_CONNECTION_STRING

    return None
