#!/bin/bash

function dependencies_error(){
    echo "failed openvpn build dependencies installation" && exit 1
}

# asking if obsfuscated server support is required
echo "Do you want to install support for obfuscated servers (it will reinstall openvpn)?[y/n] (Recommended: n)"
read ANSWER
if [ "$ANSWER" = "Y" ] ; then ANSWER=y; fi;
if [ "$ANSWER" = "N" ] ; then ANSWER=n; fi;

# clearing downloaded .ovpn
rm -rf ovpn_*

# installing openvpn (either from source or with system package manager)
if [ "$ANSWER" = 'y' ]
then sudo apt-get remove -y openvpn || sudo dnf remove -y openvpn || sudo pacman -Rdd --noconfirm openvpn
    # installing dependencies for build
    sudo apt-get install -y gcc make automake autoconf dh-autoreconf file patch perl dh-make debhelper devscripts \
        gnupg lintian quilt libtool pkg-config libssl-dev liblzo2-dev libpam0g-dev net-tools > /dev/null ||
        sudo pacman -S --noconfirm automake autoconf gnupg quilt libtool openssl \
        lzo pam pkcs11-helper > /dev/null || sudo dnf install -y automake autoconf perl gnupg quilt libtool openssl-devel \
        lzo-devel pam-devel net-tools > /dev/null || dependencies_error

    sudo apt-get install libpkcs11-helper1-dev -y # causes sometimes dependencies errors

    ./scripts/install_patched_openvpn.sh

    wget "https://downloads.nordwebsite.net/configs/archives/servers/ovpn_xor.zip" -o /dev/null
    unzip ovpn_xor.zip > /dev/null
    mv ovpn_tcp ovpn_tcp_xor
    mv ovpn_udp ovpn_udp_xor
    rm ovpn_xor.zip

    mkdir ovpn_tcp ovpn_udp

    # linking all files into ovpn_[protocol]
    cd ovpn_tcp_xor
    for file in ./* ; do ln -s ../ovpn_tcp_xor/$file ../ovpn_tcp/$file ; done
    cd ../ovpn_udp_xor/
    for file in ./* ; do ln -s ../ovpn_udp_xor/$file ../ovpn_udp/$file ; done
    cd ..
elif [ "$ANSWER" = 'n' ]
    then
    # removing previously built version
    sudo apt-get remove openpn -y || sudo dnf remove -y openvpn || sudo pacman -R --noconfirm openvpn
    if ! [ -z `sudo which openvpn` ]; then sudo rm `sudo which openvpn`; fi;

    # installing the official version with package manager
    sudo apt-get install openvpn -y || sudo dnf install -y openvpn || sudo pacman -Sy --noconfirm openvpn ||
    (echo "Your distro is not supported, please follow README" && exit 1)
else
    echo "Invalid answer"
    exit 1
fi

# install dependencies

INSTALLATION_COMPLETED_MSG='Required packages installed'

if ! [ -z `which apt-get 2> /dev/null` ]; # Debian
    then sudo apt-get install -y python3 python3-tk python3-requests wget strongswan strongswan-ikev2 \
    libstrongswan-standard-plugins unzip libstrongswan-extra-plugins openresolv\
    libcharon-extra-plugins > /dev/null || sudo apt-get install -y python3 python3-tk python3-requests wget unzip openresolv > /dev/null
    # if some packages are missing the script try to install a minimal and fundamental set of them

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" -a "$ANSWER" = 'n' ]
    then sudo apt-get install -y network-manager-openvpn network-manager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which dnf 2> /dev/null` ]; # Fedora
    then sudo dnf install -y python3 python3-tkinter python3-requests wget unzip openresolv > /dev/null
    # sudo dnf install strongswan strongswan-charon-nm libreswan ldns unbound-libs

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" -a "$ANSWER" = 'n' ]
    then sudo dnf install -y NetworkManager-openvpn NetworkManager-openvpn-gnome > /dev/null
    fi
fi
if ! [ -z `which pacman 2> /dev/null` ]; # Arch Linux
    then sudo pacman -Sy --noconfirm python3 tk python-requests wget unzip strongswan openresolv > /dev/null||
     sudo pacman -Sy --noconfirm python3 tk python-requests wget unzip openresolv > /dev/null
    # again, the script try to install a fundamental set of packages

    echo $INSTALLATION_COMPLETED_MSG
    if [ `nmcli networking` = "enabled" -a "$ANSWER" = 'n' ]
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
