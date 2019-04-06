#!/bin/sh

# works only if launched with sudo

cd /etc/

rm resolv.conf
mv resolv.conf.backup resolv.conf
