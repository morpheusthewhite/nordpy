import json
import requests

IP_URL = "https://ipinfo.io/json"


def ip_show():
    ip_json = requests.get(IP_URL).text
    return json.loads(ip_json)['ip']


if __name__ == "__main__":
    print(ip_show())