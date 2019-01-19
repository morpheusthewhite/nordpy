from subprocess import *
from os import linesep
from bin.logging_util import get_logger
from bin.vpn_util.exceptions import LoginError

IKEV2_CREDENTIAL_FILE = '/etc/ipsec.secrets'
IKEV2_CREDENTIALS_FILE_FORMAT = '# This file holds shared secrets or RSA private keys for authentication.' + linesep + \
                                linesep + \
                          '# RSA private key for this host, authenticating it to any other host' + \
                                linesep + \
                          '# which knows the public part.' + linesep \
                                + linesep + \
                          '# this file is managed with debconf and will contain the automatically created private key' + linesep \
                                + linesep + \
                                '{username} : EAP "{password}"'

IKEV2_CONF_FILE = '/etc/ipsec.conf'
IKEV2_CONF_FILE_FORMAT = 'conn NordVPN' + linesep +\
                   '    keyexchange=ikev2' + linesep + \
                   '    dpdaction=clear' + linesep + \
                   '    dpddelay=300s' + linesep + \
                   '    eap_identity="{username}"' + linesep + \
                   '    leftauth=eap-mschapv2' + linesep + \
                   '    left=%defaultroute' + linesep + \
                   '    leftsourceip=%config' + linesep + \
                   '    right={server}' + linesep + \
                         '    rightauth=pubkey' + linesep + \
                         '    rightsubnet=0.0.0.0/0' + linesep + \
                         '    rightid=%any' + linesep + \
                         '    type=tunnel' + linesep + \
                         '    auto=add'

IKEV2_STRONGSWAN_CONF_FILE = '/etc/strongswan.d/charon/constraints.conf'
IKEV2_STRONGSWAN_CONF_FORMAT = 'constraints{' + linesep + \
                               '    # Whether to load the plugin. Can also be an integer to increase the' + linesep +\
                               '    # priority of this plugin.' + linesep +\
                               '    load = no' + linesep + \
                               '}' + linesep

logger = get_logger(__name__)

def ipsec_exists():
    """
    Verifies if ipsec is existing in the os
    :return: a boolean: True if ipsec exists, false otherwise
    """
    (_, err) = Popen(["sudo", "ipsec", "--version"], stdout=PIPE, stderr=PIPE).communicate()
    if "not found" in err:
        return False

    return True


def __ikev2_save_credentials__(username, password):
    """
    Saves the credentials in the system file
    :param username: the NordVPN account username
    :param password: the NordVPN account password
    """

    args = ['sudo', 'tee', IKEV2_CREDENTIAL_FILE]
    writing_process = Popen(args, stdout=DEVNULL, stdin=PIPE, universal_newlines=True)
    writing_process.communicate(IKEV2_CREDENTIALS_FILE_FORMAT.format(username=username, password=password))

    return


def __ikev2_save_conf_file__(username, server):
    """
    Saves the configuration for the next connection
    :param username: the NordVPN account username
    :param server: the server to which the connection will be established
    """

    args = ['sudo', 'tee', IKEV2_CONF_FILE]
    writing_process = Popen(args, stdout=DEVNULL, stdin=PIPE, universal_newlines=True)
    writing_process.communicate(IKEV2_CONF_FILE_FORMAT.format(username=username, server=server))

    return


def __ikev2_reset_load__():
    """
    Changes load setting to 'yes' in strongswan configuration file
    """

    # reading file content
    reading_args = ['sudo', 'cat', IKEV2_STRONGSWAN_CONF_FILE]
    reading_process = Popen(reading_args, stdout=PIPE, universal_newlines=True)
    (file_content, _) = reading_process.communicate()

    # only the matched content will be replaced, the rest will remain the same
    new_file_content = ''
    found = False
    for line in file_content.split(linesep):
        if 'load' in line:
            found = True
            new_file_content += line.replace('yes', 'no') + linesep
        else:
            new_file_content += line + linesep

    # the file did not contained the needed argument, file content is replaced by the default one
    if not found:
        logger.debug("Replacing "+IKEV2_STRONGSWAN_CONF_FILE+" content")
        new_file_content = IKEV2_STRONGSWAN_CONF_FORMAT

    # launching writing process
    writing_args = ['sudo', 'tee', IKEV2_STRONGSWAN_CONF_FILE]
    writing_process = Popen(writing_args, stdin=PIPE, stdout=DEVNULL, universal_newlines=True)
    writing_process.communicate(new_file_content)

    return


SUCCESS_STRING = "connection 'NordVPN' established successfully"
FAILURE_STRING = "establishing connection 'NordVPN' failed"
AUTH_FAILURE_STRING = "EAP authentication failed"


def __ikev2_launch__():
    """
    Launches the command the start the ikev2 connection. Raise a LoginError if credentials are wrong, a ConnectionError
    if no connection is available
    """
    args = ['sudo', 'ipsec', 'up', 'NordVPN']
    ipsec_start_command = Popen(args, stdout=PIPE, universal_newlines=True)

    (out, _) = ipsec_start_command.communicate()
    logger.info(out)
    if AUTH_FAILURE_STRING in out:
        raise LoginError
    elif FAILURE_STRING in out:
        raise ConnectionError

    return


def ikev2_disconnect():
    """
    Stops the ikev2 connection
    """
    args = ['sudo', 'ipsec', 'down', 'NordVPN']
    ipsec_stop_command = Popen(args, stdout=PIPE, universal_newlines=True)
    ipsec_stop_command.wait()

    return


def ikev2_is_running():
    """
    Checks if an ikev2 connection is established
    :param sudo_password: the root password
    :return: True if a connection is established, False otherwise
    """

    args = ['sudo', 'ipsec', 'status']
    ipsec_stop_command = Popen(args, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (out, _) = ipsec_stop_command.communicate()

    if 'ESTABLISHED' in out:
        logger.info("Found ikev2 connection")
        return True
    else:
        return False


def __ikev2_ipsec_reload__():
    """
    restarts ipsec (used to load saved settings)
    """
    args = ['sudo', 'ipsec', 'reload']
    (out, _) = Popen(args, stdout=PIPE, universal_newlines=True).communicate()

    if 'not running' in out:
        Popen(['sudo', 'ipsec', 'start']).communicate()

    return

def __ikev2_wait__():
    """
    wait until ikev2 is ready to establish a connection by executing a simple status
    """
    args = ['sudo', 'ipsec', 'statusall']
    Popen(args).wait()

def ikev2_connect(username, password, server):
    """
    starts a ikev2 connection. Launches a ConnectionError if no connection is available, a LoginError if the
    credentials are wrong
    :param username: the NordVPN account username
    :param password: the NordVPN account password
    :param server: the server to which the connection will be established
    :return:
    """

    # saves credentials and configurations
    __ikev2_save_credentials__(username, password)
    __ikev2_save_conf_file__(username, server)
    __ikev2_reset_load__()

    # reload ipsec configurations
    __ikev2_ipsec_reload__()

    # waiting until confs are loaded (otherwise configuration needed will not be found)
    __ikev2_wait__()
    __ikev2_wait__()

    # launches the connection
    __ikev2_launch__()

    logger.info("ikev2 connection completed")

    return
