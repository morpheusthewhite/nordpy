#!/bin/sh

# downloads the zip
wget "https://swupdate.openvpn.org/community/releases/openvpn-2.4.4.zip" -o /dev/null

# extracts it 
unzip openvpn-2.4.4.zip > /dev/null

cd openvpn-2.4.4
wget "https://raw.githubusercontent.com/clayface/openvpn_xorpatch/master/openvpn_xor.patch" -o /dev/null
git apply openvpn_xor.patch

# installing dependencies
sudo apt-get install libssl-dev liblzo2-dev libpam0g-dev build-essential -y > /dev/null

./configure > /dev/null
make > /dev/null
sudo make install > /dev/null

cd ..
echo "removing temporary files"
rm openvpn-2.4.4.zip
rm -r openvpn-2.4.4
