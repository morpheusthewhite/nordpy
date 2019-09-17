import os
from bin.root import get_root_permissions_cli
from bin.settings import correct_saved_settings, load_settings
from bin.vpn_util.networkSelection import get_recommended_server


def quick_connect():
    print("Trying to connect to the last server type")

    if os.geteuid() != 0:
        get_root_permissions_cli()

    if not correct_saved_settings():
        print("No settings stored, connect to a server type with the gui, then try again")
        return

    (server_type, protocol, country, server) = load_settings()
    protocol = int(protocol)

    server = get_recommended_server(server_type, country)

    from bin.vpn_util.openvpn import start_openvpn
    start_openvpn(server, protocol)