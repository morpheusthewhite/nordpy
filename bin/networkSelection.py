import requests
from bin.logging_util import get_logger

NORDVPN_CODES = {"Standard VPN": "11", "Double VPN": "1", "Onion over VPN": "3", "Dedicated IP": "9", "P2P": "15", "Obfuscated": "17"}
MODES = ["Standard VPN", "P2P", "Dedicated IP", "Double VPN", "Onion over VPN", "Obfuscated"]

logger = get_logger(__name__)

class RequestException(Exception):
    pass


def getRecommendedServer(serverType):
    urlRecommended = ("https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendation"
                      "s&filters={%22servers_groups%22:[", "]}")

    s = requests.Session()

    response = s.get(urlRecommended[0]+NORDVPN_CODES[serverType]+urlRecommended[1])
    # if no connection is available the get will raise a ConnectionError, catched by the calling function

    # controlling incorrect response
    if(response.status_code != 200):
        raise RequestException

    jsonData = response.text

    if jsonData == "[]":
        return None

    import json
    server = json.loads(jsonData)[0]["hostname"]

    logger.info("Connecting to " + server)
    return server


def exists_conf_for(server_name, protocol):
    import os.path
    from bin.openvpn import get_path_to_conf

    conf_filename = get_path_to_conf(server_name, protocol)
    logger.debug("Checking if exists "+conf_filename)

    return os.path.exists(conf_filename)


# download from nordvpn.com all conf files and stores them in the current directory
def update_conf_files(sudo_password):
    import subprocess
    from bin.root import getRootPermissions
    from bin.pathUtil import CURRENT_PATH

    getRootPermissions(sudo_password)

    logger.debug("Missing files, trying to download the .ovpn files")
    ovpn_download_link = 'https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip'
    zip_filename = CURRENT_PATH + 'ovpn.zip'

    # downloading the zipped files
    r = requests.get(ovpn_download_link, allow_redirects=True)
    with open(zip_filename, 'wb') as zip_f:
        zip_f.write(r.content)

    args1 = ['unzip', zip_filename]
    unzipping = subprocess.Popen(args1, universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    unzipping.communicate("A\n")    # if files already exist they are replaced [A]ll

    # waiting for unzip to complete
    unzipping.wait()

    # removing zip
    from os import remove
    remove(zip_filename)

    logger.debug("Finished preparing ovpn files")

    return
