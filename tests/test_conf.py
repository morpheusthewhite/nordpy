from bin.conf_util import *


def test_get_path():
    assert get_path_to_conf("nl833.nordvpn.com", 1).endswith(
        "ovpn_tcp/nl833.nordvpn.com.tcp.ovpn")


def test_update_conf():
    with open(update_conf("ovpn_tcp/nl833.nordvpn.com.tcp.ovpn", {"ping-restart": 10}), 'r') as new_conf:
        assert("ping-restart 10" in new_conf.read())
