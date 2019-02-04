#!/bin/bash

# install dependencies

if ! [ -z `which apt-get 2> /dev/null` ]; # Debian
    then sudo apt-get install python3 python3-tk python3-requests openvpn wget strongswan strongswan-ikev2 \
    libstrongswan-standard-plugins unzip libstrongswan-extra-plugins \
    libcharon-extra-plugins
    if [ `nmcli networking` = "enabled" ]
    then sudo apt-get install network-manager-openvpn network-manager-openvpn-gnome
    fi
fi
if ! [ -z `which dnf 2> /dev/null` ]; # Fedora
    then sudo dnf install python3 python3-tkinter python3-requests openvpn wget unzip
    # sudo dnf install strongswan strongswan-charon-nm libreswan ldns unbound-libs
    if [ `nmcli networking` = "enabled" ]
    then sudo dnf install NetworkManager-openvpn NetworkManager-openvpn-gnome
    fi
fi
if ! [ -z `which pacman 2> /dev/null` ]; # Arch Linux
    then sudo pacman -Sy python3 tk python-requests openvpn wget unzip strongswan
    if [ `nmcli networking` = "enabled" ]
    then sudo pacman -Sy networkmanager-openvpn
    fi
fi

# install certificates (needed by ipsec)
sudo wget https://downloads.nordvpn.com/certificates/root.der -O /etc/ipsec.d/cacerts/NordVPN.der

current_dir=`pwd`

# check which path to desktop files exists
if [ -d /usr/local/share/applications ]
then
    DESK_PATH=/usr/local/share/applications
else
    DESK_PATH=/usr/share/applications
fi
echo "Saving desktop shortcut in "$DESK_PATH

echo "[Desktop Entry]

Type=Application
Version=1.0
Name=NordPy
Comment=NordVPN client application for connecting to recommended servers
Path="$current_dir"
Exec="$current_dir"/nordpy.py
Icon="$current_dir"/media/nordvpn.png
Terminal=false
Categories=Internet;System;Utilities;" | sudo tee $DESK_PATH/nordpy.desktop > /dev/null

sudo chmod +x /usr/local/share/applications/nordpy.desktop


# downloading and extracting conf files from NordVPN
wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
unzip ovpn.zip > /dev/null
rm ovpn.zip
