from bin.vpn_util.networkSelection import *
import re


def test_recommended():
    server = get_recommended_server(MODES[0], COUNTRIES['Automatic'][0])
    print(server)
    assert re.match(".*.nordvpn.com", server)

