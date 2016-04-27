#! /bin/sh

abort()
{
    echo >&2 '
***************
*** ABORTED ***
***************
'
    echo "An error occurred. Exiting..." >&2
    exit 1
}

trap 'abort' 0

set -e
######################################################################

echo "------------------------------------------------------------------------"
echo "Configuration started......"
echo "Please run this script only once, after that delete it"
cd ~
echo "src/gz all http://repo.opkg.net/edison/repo/all" > /etc/opkg/base-feeds.conf
echo "src/gz edison http://repo.opkg.net/edison/repo/edison" >> /etc/opkg/base-feeds.conf
echo "src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" >> /etc/opkg/base-feeds.conf
# Update opkg list and install Pip
opkg update
opkg install python-pip
# This module encapsulates the access for the serial port
pip install pyserial

######################################################################
trap : 0

echo >&2 '
************
*** DONE *** 
************
'
echo "Complete."
