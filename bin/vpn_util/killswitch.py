import subprocess
import os

from bin.conf_util import get_path_to_conf, PROTOCOLS
from bin.logging_util import get_logger
from bin.pathUtil import CURRENT_PATH

TABLES_FILENAME = 'stored_iptables'
logger = get_logger(__name__)


def check_has_legacy():
    (out, _) = subprocess.Popen(["iptables-legacy", "-h"],
                                stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()
    if len(out) == 0:
        return False
    else:
        return True


has_legacy = check_has_legacy()


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
            return line.split()[1:3]


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


def get_network(interface):
    """
    :return: the address of the network to which the host belongs (on the given interface)
    """
    (out, _) = subprocess.Popen(['ip', 'r'], stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()

    lines = out.split(os.linesep)
    for line in lines:
        line_splitten = line.split()

        # look for the interface name to get the network address (which is the first field)
        if len(line_splitten) > 0 and line_splitten[2] == interface:
            return line_splitten[0]


def iptables_save():
    """
    save the current iptables
    """
    # load the module needed to output correctly the state of the iptables
    subprocess.Popen(["sudo", "modprobe", "iptable_filter"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).communicate()

    if has_legacy:
        args = ["sudo", "iptables-legacy-save"]
    else:
        args = ["sudo", "iptables-save"]

    (out, _) = subprocess.Popen(args, stdout=subprocess.PIPE,
                                universal_newlines=True).communicate()
    with open(os.path.join(CURRENT_PATH, TABLES_FILENAME), 'w') as f:
        f.write(out)

    return


def iptables_restore():
    """
    restore previously saved iptables
    """
    tables_file = os.path.join(CURRENT_PATH, TABLES_FILENAME)
    logger.info("looking for iptables in " + tables_file)

    if has_legacy:
        args = ["sudo", "iptables-legacy-restore", tables_file]
    else:
        args = ["sudo", "iptables-restore", tables_file]

    subprocess.Popen(args).communicate()

    try:
        os.remove(tables_file)
    except FileNotFoundError:
        logger.info("No iptables to restore found")

    return


def killswitch_up(server_name, protocol):
    iptables_save()

    interface = get_current_used_interface()

    if interface is None:
        raise KillswitchError

    (ip, port) = read_remote_ip_port(get_path_to_conf(server_name, protocol))
    address_private_network = get_network(interface)

    logger.info("Turning on killswitch")
    logger.info("Default interface: " + interface)
    logger.info("IP and port of the VPN server: " + ip + " " + port)
    logger.info("Network address on " + interface +
                ": " + address_private_network)

    # update iptables
    subprocess.Popen(["sudo", os.path.join(CURRENT_PATH, "scripts", "ip-ks.sh"),
                      ip, port, interface, PROTOCOLS[protocol], address_private_network]).communicate()
    return


def killswitch_down():
    logger.info("Turning off killswitch")
    iptables_restore()

    return
