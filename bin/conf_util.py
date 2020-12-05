import os

import requests
from bin.logging_util import get_logger
import json
import threading
import sys
import random


from bin.pathUtil import CURRENT_PATH

logger = get_logger(__name__)
XOR_OVPN_FOLDER = "ovpn_{protocol}_xor"


def exists_conf_for(server_name, protocol):
    """
    Checks if exists a .ovpn file for the specified server and protocol
    :param server_name: the name of the server
    :param protocol: the protocol to be used
    :return: True if exists, False otherwise
    """
    import os.path

    conf_filename = get_path_to_conf(server_name, protocol)
    logger.debug("Checking if exists "+conf_filename)

    return os.path.exists(conf_filename)


def update_conf_files():
    """
    Downloads from nordvpn.com all the .ovpn files
    """
    from bin.pathUtil import CURRENT_PATH

    logger.debug("Missing files, trying to download the .ovpn files")
    ovpn_download_link = 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'
    zip_filename = CURRENT_PATH + 'ovpn.zip'

    # downloading the zipped files
    r = requests.get(ovpn_download_link, allow_redirects=True)
    with open(zip_filename, 'wb') as zip_f:
        zip_f.write(r.content)

    # unzipping files
    import zipfile
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(CURRENT_PATH)

    # removing zip
    from os import remove
    remove(zip_filename)

    logger.debug("Finished preparing ovpn files")


def get_available_servers():
    """
    returns a list of all available server
    :return: a list with all the server names
    """
    import os.path
    from bin.pathUtil import CURRENT_PATH

    servers_entire_name = os.listdir(CURRENT_PATH + "ovpn_tcp/")
    servers = []
    for server in servers_entire_name:
        servers.append(server.split(".")[0])
    servers.sort()
    return servers[:40]


def get_available_servers_dict():
    """
    returns a list of all available server as a dictionary whose keys are the countries
    :return: a dictionary
    """
    import os.path
    from bin.pathUtil import CURRENT_PATH

    def get_server_domain(server):
        numbers = '1234567890'
        domain = ''

        for letter in server:
            if letter not in numbers:
                domain += letter
            else:
                break

        return domain

    servers_entire_names = os.listdir(CURRENT_PATH + "ovpn_tcp/")
    servers = {}

    for server in servers_entire_names:
        domain_name = get_server_domain(server)

        try:
            servers[domain_name].append(server.split(".")[0])
        except KeyError:
            servers[domain_name] = [server.split(".")[0]]

    # sorts all servers
    for server_domain in servers.keys():
        servers[server_domain].sort()

    return servers


STATS_URL = 'https://nordvpn.com/api/server/stats'
PERCENT_KEY = 'percent'


class StatsHolder:
    def __init__(self):
        threading.Thread(target=self.stats_parallel_request).start()

        self.stats_dic = {}

    def stats_parallel_request(self):
        try:
            stats = requests.get(STATS_URL)
        except requests.ConnectionError:
            return

        parser = json.decoder.JSONDecoder()
        self.stats_dic = parser.decode(stats.text)
        logger.debug("Retrieved stats")

    def get_server_stats_as_str(self, server):
        """
        returns the load of a specific server
        :param server: the server whose load is needed
        :return: the load as a string (with percent character)
        """
        try:
            return str(self.stats_dic[server+".nordvpn.com"][PERCENT_KEY])+"%"
        except KeyError:
            return ""

    def get_server_stats_as_int(self, server):
        """
        returns the load of a specific server
        :param server: the server whose load is needed (in the form xxx.nordvpn.com)
        :return: the load as int. Raises a ConnectionError if no connection is available; raises a KeyError
        is the stats for the requested server are not available
        """
        if self.stats_dic == {}:
            raise requests.ConnectionError

        return self.stats_dic[server][PERCENT_KEY]

    def has_stats(self):
        """
        :return: true if some stats are saved, false otherwise
        """
        return self.stats_dic != {}


# retrieve stats iff nordpy is opened with gui
if 'bin.command_line_util' not in sys.modules.keys() and 'bin.gui' in sys.modules.keys():
    global_stats_holder = StatsHolder()

    # updating stats in another thread
    threading.Thread(target=global_stats_holder.stats_parallel_request).start()


def get_path_to_conf(server, protocol):
    """
    calculates the path to the .ovpn file from the given server and protocol
    :param server: the name of the server
    :param protocol: the protocol to be used
    :return: the path to the file
    """
    return os.path.join(CURRENT_PATH + "ovpn_" + PROTOCOLS[protocol], server + "." + PROTOCOLS[protocol] + OVA_SUFFIX)


def update_conf(conf_filepath: str, settings: dict):
    """
    create a new temporary configuration file with the new updated settings
    :param conf_filepath: the path of the original configuration file
    :param settings: a dictionary containing the key to change and its new value
    :return: the path to the new (temporary) configuration file
    """
    new_conf_filepath = "/tmp/_nordpy" + str(random.randint(0, 1000))

    # replace just the needed lines, copy the others
    with open(conf_filepath, 'r') as old_conf:
        with open(new_conf_filepath, 'w') as new_conf:
            for line in old_conf:
                key = line.strip().split(" ")[0]
                if settings.get(key):
                    new_conf.write(str(key) + " " + str(settings[key]) + os.linesep)
                    settings.pop(key)
                else:
                    new_conf.write(line)

    return new_conf_filepath


OVA_SUFFIX = ".ovpn"
PROTOCOLS = ["udp", "tcp", "Ikev2/IPsec"]
