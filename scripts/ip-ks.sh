#!/bin/bash

# accepted argument (in order)
# 1: remote ip of the VPN server
# 2: remote port of the VPN server
# 3: name of the interface in use
# 4: protocol (tcp or udp) to be used (lowercase)
# 5: address of the network on the chosen interface

EXPECTED_ARGC=5

if [ $# -ne $EXPECTED_ARGC ]
then
    echo "Incorrect number of arguments"
    exit
fi

REMOTE_IP=$1
REMOTE_PORT=$2
INTERFACE=$3
PROTOCOL=$4
NETWORK_ADDRESS=$5

echo "Launching $PROTOCOL connection with $REMOTE_IP:$REMOTE_PORT on $INTERFACE (on network $5)"

# clear tables
iptables-legacy --flush
iptables-legacy --delete-chain
iptables-legacy -t nat --flush
iptables-legacy -t nat --delete-chain

# general policy
iptables-legacy -P OUTPUT DROP
iptables-legacy -P INPUT DROP

# localhost
iptables-legacy -A INPUT -j ACCEPT -i lo
iptables-legacy -A OUTPUT -j ACCEPT -o lo

iptables-legacy -A INPUT --src $NETWORK_ADDRESS -j ACCEPT -i $INTERFACE
iptables-legacy -A OUTPUT -d $NETWORK_ADDRESS -j ACCEPT -o $INTERFACE
iptables-legacy -A OUTPUT -j ACCEPT -d $REMOTE_IP -o $INTERFACE -p $PROTOCOL -m $PROTOCOL --dport $REMOTE_PORT
iptables-legacy -A INPUT -j ACCEPT -s $REMOTE_IP -i $INTERFACE -p $PROTOCOL -m $PROTOCOL --sport $REMOTE_PORT
iptables-legacy -A INPUT -j ACCEPT -i tun+
iptables-legacy -A OUTPUT -j ACCEPT -o tun+
