from bin.vpn_util.ikev2 import ikev2_connect, ikev2_is_running
from bin.vpn_util.openvpn import *
from bin.root import get_root_permissions


def startVPN(server, protocol, sudoPassword):
    """
    Starts VPN with the given server and protocol. Raises a ConnectionError if no connection is available
    and a LoginError if the credentials are wrong
    :param server: the name of the server
    :param protocol: the protocol to be used
    :param sudoPassword: the root password
    :return: a Popen object if a openvpn started successfully, None if it is an ikev2
    """
    get_root_permissions(sudoPassword)

    if not check_credentials():
        try:
            save_credentials()
        except NoCredentialsProvidedException:
            return None

    if protocol == 2:  # if it is ikev2/ipvsec
        username, password = read_saved_credentials(sudoPassword)
        ikev2_connect(sudoPassword, username, password, server)
    else:
        start_openvpn(server, protocol)


def is_vpn_running():
    return checkOpenVPN()
