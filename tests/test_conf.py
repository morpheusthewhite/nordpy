from bin.conf_util import *


def test_get_path():
    """
    Return the path to the test config file.

    Args:
    """
    assert get_path_to_conf("ar20.nordvpn.com", 1).endswith("ovpn_tcp/ar20.nordvpn.com.tcp.ovpn")


def test_update_conf():
    """
    Update the current configuration file.

    Args:
    """
    with open(update_conf("ovpn_tcp/ar20.nordvpn.com.tcp.ovpn", {"ping-restart": 10}), 'r') as new_conf:
        assert("ping-restart 10" in new_conf.read())