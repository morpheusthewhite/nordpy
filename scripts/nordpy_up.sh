#!/bin/sh

# works only if launched with sudo

cd /etc/
printf "# Appended by NordPy\nnameserver 103.86.96.100\nnameserver 103.86.99.100\n" > resolv.conf.tmp && sed '/nameserver/ d' resolv.conf >> resolv.conf.tmp

mv resolv.conf resolv.conf.backup
mv resolv.conf.tmp resolv.conf
