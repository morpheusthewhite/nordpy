import subprocess
from os import linesep

from bin.vpn_util.exceptions import LoginError
from bin.vpn_util.openvpn import get_path_to_conf
from bin.conf_util import PROTOCOLS
from bin.logging_util import get_logger

logger = get_logger(__name__)
NM_TIMEOUT = 10


def get_connection_name(server, protocol):
    """
    returns the name of the connection given the name of the server and the protocol used
    :param server: the name of the server
    :param protocol: an integer representing the protocol to be used
    :return: the name of the connection as is used in nm
    """
    return server + '.' + PROTOCOLS[protocol]


def nm_list_vpn():
    """
    finds all the name of the available vpn connections
    :return: a list containing the name of all the imported vpn connections
    """
    args = ['nmcli', 'conn']
    list_process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE)

    (out, _) = list_process.communicate()

    vpns = []
    for line in out.split(linesep):
        words = line.split()

        # usually the third column contains the type
        if len(words) > 2 and words[2] == 'vpn' and 'nordvpn' in words[0]:
            vpns.append(words[0])

    return vpns


def nm_delete(connection_list):
    """
    removes imported connections
    :param connection_list: the list of name of the connections that will be removed
    """
    args = ['nmcli', 'connection', 'delete'] + connection_list

    subprocess.Popen(args).wait()

    return


def nm_stop(connection_name):
    """
    stops a connection with a given name
    :param connection_name: the name of the connection that will be stopped
    """
    args = ['nmcli', 'connection', 'down', connection_name]

    subprocess.Popen(args).wait()
    return


def nm_launch(connection_name, password):
    """
    starts a connection with a given name
    :param connection_name: the name of the connection that will be started
    :param password: the password of the nordVPN account
    """
    args = ['nmcli', '--ask', '--wait', str(NM_TIMEOUT), 'connection', 'up', connection_name]

    (out, err) = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True).communicate(password + linesep)

    if 'A password is required.' in out:
        # that text is found if and only if the password inserted was wrong (it is requested for the second time)
        raise LoginError

    if 'Error' in err:
        raise ConnectionError

    return


def nm_set_credentials(username, connection_name):
    """
    starts a connection with a given name
    :param username: the username of the NordVPN account
    :param connection_name: the name of the connection that will be started
    """
    args = ['nmcli', 'connection', 'modify', connection_name, '+vpn.data', 'username='+username]

    subprocess.Popen(args).wait()
    return


def nm_import(openvpn_file):
    """
    imports into the network manager the given file
    :param openvpn_file: the path to the file to be imported
    """
    args = ['nmcli', 'connection', 'import', 'type', 'openvpn', 'file', openvpn_file]

    subprocess.Popen(args).wait()
    return


def nm_openvpn_exists():
    """
    Verifies if nmcli-openvpn is existing in the os
    :return: a boolean: True if it exists, false otherwise
    """
    (_, err) = subprocess.Popen(["nmcli", "--version"], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, universal_newlines=True).communicate()
    if "command not found" in err or "failed to find VPN plugin" in err:
        return False

    (out, _) = subprocess.Popen(["nmcli", "networking"], stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()
    if "enabled" not in out:
        # network manager is installed but it is not enabled by default
        return False

    return True


def nm_running_vpn():
    """
    checks if some vpn is running
    :return: False if no connection to vpn are running, the name of the connection otherwise
    """
    args = ['nmcli', 'conn', 'show', '--active']
    list_process = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE)

    (out, _) = list_process.communicate()

    for line in out.split(linesep):
        words = line.split()

        # usually the third column contains the type
        if len(words) > 2 and words[2] == 'vpn' and 'nordvpn' in words[0]:
            return words[0]

    return False


def nm_disconnect():
    """
    disconnect the running connection to vpn
    """
    connection_name = nm_running_vpn()

    if connection_name is False:
        return

    nm_stop(connection_name)


def nm_connect(server, protocol, username, password):
    """
    Starts a connection to a particular server through nm
    :param server: the name of the server
    :param protocol: the protocol to be used (an integer between 1 and 0)
    """
    # removing imported vpns
    nm_delete(nm_list_vpn())

    pathToConf = get_path_to_conf(server, protocol)
    connection_name = get_connection_name(server, protocol)

    logger.info('Importing and configuring ' + pathToConf)

    # preparing connection
    nm_import(pathToConf)
    nm_set_credentials(username, connection_name)

    nm_launch(connection_name, password)
