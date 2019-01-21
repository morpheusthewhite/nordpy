from requests import get
from bin.logging_util import get_logger

AUTOMATIC_CHOICE_STRING = 'Choose Automatically'
NORDVPN_CODES = {"Standard VPN": "11", "Double VPN": "1", "Onion over VPN": "3", "Dedicated IP": "9", "P2P": "15", "Obfuscated": "17"}
MODES = ["Standard VPN", "P2P", "Dedicated IP", "Double VPN", "Onion over VPN", "Obfuscated"]
COUNTRIES = {'Automatic': [AUTOMATIC_CHOICE_STRING],
             'Africa': ['South Africa', 'Egypt'],
             'Asia': ['Turkey', 'Israel', 'United Arab Emirates', 'India', 'South Korea', 'Singapore', 'Taiwan', 'Vietnam',
                      'Hong Kong', 'Indonesia', 'Thailand', 'Japan', 'Malaysia'],
             'America': ['United States', 'Canada', 'Mexico', 'Brazil', 'Costa Rica', 'Argentina', 'Chile'],
             'Europe': ['United Kingdom', 'Netherlands', 'Germany', 'France', 'Belgium', 'Switzerland', 'Sweden',
                        'Spain', 'Denmark', 'Italy', 'Norway', 'Austria', 'Romania', 'Czech Republic', 'Luxembourg',
                        'Poland', 'Finland', 'Hungary', 'Latvia', 'Russia', 'Iceland', 'Bulgaria', 'Croatia', 'Moldova',
                        'Portugal', 'Albania', 'Ireland', 'Slovakia', 'Ukraine', 'Cyprus', 'Estonia', 'Georgia', 'Greece',
                        'Serbia', 'Slovenia', 'Azerbaijan', 'Bosnia and Herzegovina', 'Macedonia'],
             'Oceania': ['Australia', 'New Zealand']
             }
COUNTRY_CODES={"Albania": 2,"Argentina": 10,"Australia": 13,"Austria": 14,"Azerbaijan": 15,"Belgium": 21,
               "Bosnia and Herzegovina": 27,"Brazil": 30,"Bulgaria": 33,"Canada": 38,"Chile": 43,"Costa Rica": 52,
               "Croatia": 54,"Cyprus": 56,"Czech Republic": 57,"Denmark": 58,"Egypt": 64,"Estonia": 68,
               "Finland": 73,"France": 74,"Georgia": 80,"Germany": 81,"Greece": 84,"Hong Kong": 97,"Hungary": 98,
               "Iceland": 99,"India": 100,"Indonesia": 101,"Ireland": 104, "Israel": 105,"Italy": 106,"Japan": 108,
               "South Korea": 114,"Latvia": 119,"Luxembourg": 126,"Macedonia": 128,"Malaysia": 131,
               "Mexico": 140,"Moldova": 142,"Netherlands": 153,"New Zealand": 156,"Norway": 163,
               "Poland": 174,"Portugal": 175,"Romania": 179,"Russia": 180,"Serbia": 192,"Singapore": 195,
               "Slovakia": 196,"Slovenia": 197,"South Africa": 200,"Spain": 202,"Sweden": 208,"Switzerland": 209,
               "Taiwan": 211,"Thailand": 214,"Turkey": 220,"Ukraine": 225,"United Kingdom": 227,
               "United States": 228,"United Arab Emirates":226,"Vietnam": 234}
STD_HEADERS = {'user-agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
logger = get_logger(__name__)


class RequestException(Exception):
    pass


def get_recommended_server(server_type, country):
    """
    Obtains the recommended server of a certain type in a given country according to NordVPN.com. Raises a
    RequestException if NordVPN's response is incorrect
    :param server_type: the type of the server (such as Obfuscated IP)
    :param country: the country (can be chosen automatically)
    :return: the recommmended server
    """
    response = get(get_nordvpn_url(server_type, country), headers=STD_HEADERS)
    # if no connection is available the get will raise a ConnectionError, catched by the calling function

    # controlling incorrect response
    if response.status_code != 200:
        raise RequestException

    jsonData = response.text

    if jsonData == "[]":
        return None

    import json
    server = json.loads(jsonData)[0]["hostname"]

    logger.info("Connecting to " + server)
    return server


def get_nordvpn_url(server_type, country):
    """
    Builds the url to obtain the recommended server from NordVPN
    :param server_type: the string representing the type of the server requested
    :param country: the string representing the country requested
    :return: the build to which the request must be sent to retrieve the recommended server
    """

    base_url = "https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations&filters=" \
               "{{{server_type}{country}}}"
    server_type_filter = "%22servers_groups%22:{server_code}"
    country_filter = "%22country_id%22:{country_code}"

    server_type_filter_formatted = server_type_filter.format(server_code=NORDVPN_CODES[server_type])

    if country == COUNTRIES['Automatic'][0]:
        resulting_url = base_url.format(server_type=server_type_filter_formatted, country='')
    else:
        logger.debug("Selected a particular country: "+country)
        country_filter_formatted = ","+country_filter.format(country_code=COUNTRY_CODES[country])
        resulting_url = base_url.format(server_type=server_type_filter_formatted, country=country_filter_formatted)

    logger.debug("resulting url: "+resulting_url)
    return resulting_url

