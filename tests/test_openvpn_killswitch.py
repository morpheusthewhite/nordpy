from bin.vpn_util.openvpn import start_openvpn, openvpn_stop, checkOpenVPN
from bin.root import get_root_permissions_cli
from .ip_show import ip_show

TEST_SERVER="us3381.nordvpn.com"
TEST_PROTOCOL = 0

get_root_permissions_cli()

initial_ip = ip_show()


def test_status_before_connection():
    assert not checkOpenVPN()


def test_start_connection():
    start_openvpn(TEST_SERVER, TEST_PROTOCOL, True)
    assert initial_ip != ip_show()


def test_status_after_connection():
    assert checkOpenVPN()


def test_stop_connection():
    openvpn_stop(True)
    assert initial_ip == ip_show()

