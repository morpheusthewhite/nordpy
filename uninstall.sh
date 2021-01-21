#!/bin/bash

# clearing downloaded .ovpn
rm -rf ovpn_*

# remove previous link
sudo rm /usr/local/bin/nordpy 2> /dev/null

xdg-desktop-menu uninstall --novendor nordpy.desktop

