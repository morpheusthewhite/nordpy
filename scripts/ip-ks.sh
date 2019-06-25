#!/bin/bash

# accepted argument (in order)
# 1: remote ip of the VPN server
# 2: remote port of the VPN server
# 3: name of the interface in use
# 4: protocol (tcp or udp) to be used (lowercase)

EXPECTED_ARGC=4

if [ $# -ne $EXPECTED_ARGC ]
    then
    echo "Incorrect number of arguments"
    exit
fi

REMOTE_IP=$1
REMOTE_PORT=$2
INTERFACE=$3
PROTOCOL=$4

# clear tables
iptables --flush
iptables --delete-chain
iptables -t nat --flush
iptables -t nat --delete-chain

# general policy
iptables -P OUTPUT DROP

# localhost
iptables -A INPUT -j ACCEPT -i lo
iptables -A OUTPUT -j ACCEPT -o lo

iptables -A INPUT --src 192.168.0.0/24 -j ACCEPT -i $INTERFACE
iptables -A OUTPUT -d 192.168.0.0/24 -j ACCEPT -o $INTERFACE
iptables -A OUTPUT -j ACCEPT -d $REMOTE_IP -o $INTERFACE -p $PROTOCOL -m $PROTOCOL --dport $REMOTE_PORT
iptables -A INPUT -j ACCEPT -s $REMOTE_IP -i $INTERFACE -p $PROTOCOL -m $PROTOCOL --sport $REMOTE_PORT
iptables -A INPUT -j ACCEPT -i tun
iptables -A OUTPUT -j ACCEPT -o tun