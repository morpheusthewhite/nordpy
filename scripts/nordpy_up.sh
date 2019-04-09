#!/bin/sh

# works only if launched with sudo

cd /etc/
printf "# Appended by NordPy\nnameserver 8.8.8.8\nnameserver 8.8.4.4\n" > resolv.conf.tmp && sed '/nameserver/ d' resolv.conf >> resolv.conf.tmp

mv resolv.conf resolv.conf.backup
mv resolv.conf.tmp resolv.conf
