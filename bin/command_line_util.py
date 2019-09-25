import os
from bin.root import get_root_permissions_cli
from bin.settings import correct_saved_settings, load_settings
from bin.vpn_util.networkSelection import get_recommended_server
from bin.vpn_util.openvpn import start_openvpn, openvpn_stop, checkOpenVPN


def quick_connect(wait_connection=False, sleep_time=5):
    print("Trying to connect to the last server type")

    if os.geteuid() != 0:
        get_root_permissions_cli()

    if not correct_saved_settings():
        print("No settings stored, connect to a server type with the gui, then try again")
        return

    (server_type, protocol, country, server) = load_settings()
    protocol = int(protocol)

    # wait until a connection is established
    if wait_connection:
        import requests
        import time
        while True:
            try:
                requests.get("http://216.58.192.142")  # get google.com
                break
            except requests.exceptions.ConnectionError:
                time.sleep(sleep_time)

    server = get_recommended_server(server_type, country)

    start_openvpn(server, protocol)


def quick_disconnect():
    print("Shutting down any nordpy VPN connection")

    openvpn_stop()


def status(all=False):
    """
    Check VPN status
    :param all: if true, check among all type of connection; if false check only openvpn
    :return: "Enabled" if a VPN connection is running, "Disabled" otherwise
    """
    if not all:
        if checkOpenVPN():
            return "Enabled"
        else:
            return "Disabled"
    else:
        from bin.vpn_util.vpn import get_running_vpn
        if get_running_vpn() is not None:
            return "Enabled"
        else:
            return "Disabled"
