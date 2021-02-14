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

# if a iptables-legacy command is available, use it
if [[ -z $(iptables-legacy -h) ]] ; then
    IPTABLES=iptables
else
    IPTABLES=iptables-legacy
fi

# clear tables
${IPTABLES} --flush
${IPTABLES} --delete-chain
${IPTABLES} -t nat --flush
${IPTABLES} -t nat --delete-chain

# general policy
${IPTABLES} -P OUTPUT DROP
${IPTABLES} -P INPUT DROP

# localhost
${IPTABLES} -A INPUT -j ACCEPT -i lo
${IPTABLES} -A OUTPUT -j ACCEPT -o lo

${IPTABLES} -A INPUT --src $NETWORK_ADDRESS -j ACCEPT -i $INTERFACE
${IPTABLES} -A OUTPUT -d $NETWORK_ADDRESS -j ACCEPT -o $INTERFACE
${IPTABLES} -A OUTPUT -j ACCEPT -d $REMOTE_IP -o $INTERFACE -p $PROTOCOL -m $PROTOCOL --dport $REMOTE_PORT
${IPTABLES} -A INPUT -j ACCEPT -s $REMOTE_IP -i $INTERFACE -p $PROTOCOL -m $PROTOCOL --sport $REMOTE_PORT
${IPTABLES} -A INPUT -j ACCEPT -i tun+
${IPTABLES} -A OUTPUT -j ACCEPT -o tun+
