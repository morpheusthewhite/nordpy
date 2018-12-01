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
