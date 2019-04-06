#!/bin/bash

# install dependencies

INSTALLATION_COMPLETED_MSG='Required packages installed'

if ! [ -z `which apt-get 2> /dev/null` ]; # Debian
    then sudo apt-get install -y python3 python3-tk python3-requests openvpn wget strongswan strongswan-ikev2 \
    libstrongswan-standard-plugins unzip libstrongswan-extra-plugins\
    libcharon-extra-plugins > /dev/null || sudo apt-get install -y python3 python3-tk python3-requests openvpn wget unzip> /dev/null
    # if some packages are missing the script try to install a minimal and fundamental set of them

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo apt-get install -y network-manager-openvpn network-manager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which dnf 2> /dev/null` ]; # Fedora
    then sudo dnf install -y python3 python3-tkinter python3-requests openvpn wget unzip> /dev/null
    # sudo dnf install strongswan strongswan-charon-nm libreswan ldns unbound-libs

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo dnf install -y NetworkManager-openvpn NetworkManager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which pacman 2> /dev/null` ]; # Arch Linux
    then sudo pacman -Sy --noconfirm python3 tk python-requests openvpn wget unzip strongswan > /dev/null||
     sudo pacman -Sy --noconfirm python3 tk python-requests openvpn wget unzip > /dev/null
    # again, the script try to install a fundamental set of packages

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo pacman -Sy --noconfirm networkmanager-openvpn > /dev/null
    fi
fi

echo "installing certificates (needed by ipsec)"
sudo wget https://downloads.nordvpn.com/certificates/root.der -O /etc/ipsec.d/cacerts/NordVPN.der -o /dev/null

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
Path=$current_dir
Exec=\"$current_dir/nordpy.py\"
Icon=$current_dir/media/nordvpn.png
Terminal=false
Categories=Internet;System;Utilities;" | sudo tee $DESK_PATH/nordpy.desktop > /dev/null

sudo chmod +x $DESK_PATH/nordpy.desktop

echo "downloading and extracting conf files from NordVPN"
wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip -o /dev/null
unzip ovpn.zip > /dev/null
rm ovpn.zip
