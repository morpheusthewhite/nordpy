from bin.vpn_util.ikev2 import ikev2_connect, ikev2_is_running, ikev2_disconnect, ipsec_exists
from bin.vpn_util.openvpn import *
from bin.vpn_util.nm import nm_running_vpn, nm_disconnect, nm_connect, nm_openvpn_exists
IPSEC_EXISTS = ipsec_exists()


def startVPN(server, protocol, nm):
    """
    Starts VPN with the given server and protocol. Raises a ConnectionError if no connection is available
    and a LoginError if the credentials are wrong
    :param server: the name of the server
    :param protocol: the protocol to be used
    :param nm: a boolean: True if network manager should be used, false otherwise
    :return: a Popen object if a openvpn started successfully, None if it is an ikev2
    """
    if not check_credentials():
        try:
            save_credentials()
        except NoCredentialsProvidedException:
            return None

    username, password = read_saved_credentials()

    if protocol == IKEV2_PROTOCOL_NUMBER:  # if it is ikev2/ipvsec
        ikev2_connect(username, password, server)
    elif nm and nm_openvpn_exists():
        nm_connect(server, protocol, username, password)
    else:
        start_openvpn(server, protocol)


def stop_vpn(running_connection):
    if running_connection == OPENVPN_CONNECTION_STRING:
        subprocess.call(["sudo", "killall", "openvpn"])
    elif running_connection == IPSEC_CONNECTION_STRING:
        ikev2_disconnect()
    elif running_connection == NM_CONNECTION_STRING:
        nm_disconnect()

    return

OPENVPN_CONNECTION_STRING = 'UDP/TCP'
IPSEC_CONNECTION_STRING = 'Ikev2'
NM_CONNECTION_STRING = 'UDP/TCP (nm)'


def get_running_vpn():
    """
    checks if some type of VPN connection is already running
    :return: a string representing what is running, None otherwise
    """
    if checkOpenVPN():
        return OPENVPN_CONNECTION_STRING
    elif ikev2_is_running():
        return IPSEC_CONNECTION_STRING
    elif nm_running_vpn():
        return NM_CONNECTION_STRING

    return None
