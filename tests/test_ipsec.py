from bin.vpn_util import ikev2
from tests.ip_show import ip_show 
from bin import root
from bin import credentials

TEST_SERVER="us3381.nordvpn.com"


initial_ip = ip_show()

root.get_root_permissions_cli()


def test_ipsec_connection():
    server = TEST_SERVER
    (username, password) = credentials.read_saved_credentials()

    ikev2.ikev2_connect(username, password, server)
    assert not ip_show() == initial_ip


def test_ipsec_disconnection():
    ikev2.ikev2_disconnect()

    assert ip_show() == initial_ip

