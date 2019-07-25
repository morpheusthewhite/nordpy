import subprocess
import os

from bin.conf_util import get_path_to_conf, PROTOCOLS
from bin.logging_util import get_logger

TABLES_FILENAME = 'stored_iptables'
logger = get_logger(__name__)


class KillswitchError(RuntimeError):
    pass


def read_remote_ip_port(ovpn_filename):
    """
    Return ip and port of the remote defined in the ovpn_filename
    """

    with open(ovpn_filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "remote" in line:
            return line.split()[1:]


def get_current_used_interface():
    """
    :return: the name of the used interface for connection
    """
    (out, _) = subprocess.Popen(["sudo", "route"], stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()

    lines = out.split(os.linesep)
    for line in lines:
        line_splitten = line.split()

        # look for the default route to get interface name
        if len(line_splitten) > 0 and line_splitten[0] == "default":
            return line_splitten[-1]


def iptables_save():
    """
    save the current iptables
    """
    (out, _) = subprocess.Popen(["sudo", "iptables-save"], stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()

    with open(TABLES_FILENAME, 'w') as f:
        f.write(out)

    return


def iptables_restore():
    """
    restore previously saved iptables
    """
    subprocess.Popen(["sudo", "iptables-restore", TABLES_FILENAME]).communicate()

    try:
        os.remove(TABLES_FILENAME)
    except FileNotFoundError:
        pass

    return


def killswitch_up(server_name, protocol):
    iptables_save()

    interface = get_current_used_interface()

    if interface is None:
        raise KillswitchError

    (ip, port) = read_remote_ip_port(get_path_to_conf(server_name, protocol))

    logger.info("Turning on killswitch")

    # update iptables
    subprocess.Popen(["sudo", os.path.join("scripts", "ip-ks.sh"),
                      ip, port, interface, PROTOCOLS[protocol]]).communicate()
    return


def killswitch_down():
    logger.info("Turning off killswitch")
    iptables_restore()

    return
