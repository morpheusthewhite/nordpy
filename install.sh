#!/bin/bash

# install dependencies

if ! [ -z `which apt-get 2> /dev/null` ]; # Debian
    then sudo apt-get install python3 python3-tk python3-requests openvpn wget strongswan strongswan-ikev2 \
    libstrongswan-standard-plugins unzip libstrongswan-extra-plugins openresolv\
    libcharon-extra-plugins || sudo apt-get install python3 python3-tk python3-requests openvpn wget unzip openresolv
    # if some packages are missing the script try to install a minimal and fundamental set of them

    if [ `nmcli networking` = "enabled" ]
    then sudo apt-get install network-manager-openvpn network-manager-openvpn-gnome
    fi
fi
if ! [ -z `which dnf 2> /dev/null` ]; # Fedora
    then sudo dnf install python3 python3-tkinter python3-requests openvpn wget unzip openresolv
    # sudo dnf install strongswan strongswan-charon-nm libreswan ldns unbound-libs
    if [ `nmcli networking` = "enabled" ]
    then sudo dnf install NetworkManager-openvpn NetworkManager-openvpn-gnome
    fi
fi
if ! [ -z `which pacman 2> /dev/null` ]; # Arch Linux
    then sudo pacman -Sy python3 tk python-requests openvpn wget unzip strongswan openresolv ||
     sudo pacman -Sy python3 tk python-requests openvpn wget unzip openresolv
    # again, the script try to install a fundamental set of packages

    if [ `nmcli networking` = "enabled" ]
    then sudo pacman -Sy networkmanager-openvpn
    fi
fi

# downloading update-resolv-conf to prevent dns leaks
UPDATE_RESOLV_CONF_URL='https://raw.githubusercontent.com/alfredopalhares/openvpn-update-resolv-conf/master/update-resolv-conf.sh'
sudo wget $UPDATE_RESOLV_CONF_URL -O /etc/openvpn/update-resolv-conf && sudo chmod +x /etc/openvpn/update-resolv-conf

# fixing resolv.conf conflicts between NetworkManager and openresolv
if [ `nmcli networking` = "enabled" ]
then echo -e "[main]\ndns=none" | sudo tee /etc/NetworkManager/conf.d/no-dns.conf > /dev/null
fi
# and using some default global dns to solve DNS_BAD_CONFIG on reboot
DNS1="208.67.222.222"  # opendns
DNS2="208.67.220.220"  # opendns
echo "\n# added to solve DNS_BAD_CONFIG by NordPy" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null
echo "prepend domain-name-servers $DNS1;" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null
echo "prepend domain-name-servers $DNS2;" | sudo tee -a /etc/dhcp/dhclient.conf > /dev/null


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
Path=$current_dir
Exec=\"$current_dir/nordpy.py\"
Icon=$current_dir/media/nordvpn.png
Terminal=false
Categories=Internet;System;Utilities;" | sudo tee $DESK_PATH/nordpy.desktop > /dev/null

sudo chmod +x $DESK_PATH/nordpy.desktop

# downloading and extracting conf files from NordVPN
wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
unzip ovpn.zip > /dev/null
rm ovpn.zip
