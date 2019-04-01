#!/bin/bash

# install dependencies

INSTALLATION_COMPLETED_MSG='Required packages installed'

if ! [ -z `which apt-get 2> /dev/null` ]; # Debian
    then sudo apt-get install -y python3 python3-tk python3-requests openvpn wget strongswan strongswan-ikev2 \
    libstrongswan-standard-plugins unzip libstrongswan-extra-plugins openresolv\
    libcharon-extra-plugins > /dev/null || sudo apt-get install -y python3 python3-tk python3-requests openvpn wget unzip openresolv > /dev/null
    # if some packages are missing the script try to install a minimal and fundamental set of them

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo apt-get install -y network-manager-openvpn network-manager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which dnf 2> /dev/null` ]; # Fedora
    then sudo dnf install -y python3 python3-tkinter python3-requests openvpn wget unzip openresolv > /dev/null
    # sudo dnf install strongswan strongswan-charon-nm libreswan ldns unbound-libs

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo dnf install -y NetworkManager-openvpn NetworkManager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which pacman 2> /dev/null` ]; # Arch Linux
    then sudo pacman -Sy --noconfirm python3 tk python-requests openvpn wget unzip strongswan openresolv > /dev/null||
     sudo pacman -Sy --noconfirm python3 tk python-requests openvpn wget unzip openresolv > /dev/null
    # again, the script try to install a fundamental set of packages

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" ]
    then sudo pacman -Sy --noconfirm networkmanager-openvpn > /dev/null
    fi
fi

echo "Downloading update-resolv-conf"
# downloading update-resolv-conf to prevent dns leaks
UPDATE_RESOLV_CONF_URL='https://raw.githubusercontent.com/alfredopalhares/openvpn-update-resolv-conf/master/update-resolv-conf.sh'
sudo wget $UPDATE_RESOLV_CONF_URL -O /etc/openvpn/update-resolv-conf -o /dev/null && sudo chmod +x /etc/openvpn/update-resolv-conf

echo "fixing resolv.conf conflicts between NetworkManager and openresolv"
if [ `nmcli networking` = "enabled" ]
then echo -e "[main]\ndns=none" | sudo tee /etc/NetworkManager/conf.d/no-dns.conf > /dev/null
fi
# and using some default global dns to solve DNS_BAD_CONFIG on reboot
GREP_RES_DHCPCONF=`grep "NordPy" /etc/dhcp/dhclient.conf`
if [ -z "$GREP_RES_DHCPCONF" ]
then DNS1="208.67.222.222"  # opendns
    DNS2="208.67.220.220"  # opendns
    echo ""
    echo "# added to solve DNS_BAD_CONFIG by NordPy" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null
    echo "prepend domain-name-servers $DNS1;" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null
    echo "prepend domain-name-servers $DNS2;" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null
fi;

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
