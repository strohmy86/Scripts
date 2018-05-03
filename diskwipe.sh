#!/bin/bash

dev="/dev/"
disk=$(lsblk | grep disk | awk '{print $1,$4}' | sort -rn -k2 | head -n 1 | cut -d " " -f1)
yep=$dev$disk
sz=$(lsblk | grep disk | awk '{print $1,$4}' | sort -rn -k2 | head -n 1 | cut -d " " -f2)

echo ""
echo "*********************************"
echo "*     Disk Wiping Utility       *"
echo "*                               *"
echo "*  Written and maintained by:   *"
echo "*        Luke Strohm            *"
echo "*    strohm.luke@gmail.com      *"
echo "*                               *"
echo "*********************************"
echo ""
echo ""

echo "The size of $yep is $sz."
echo ""
echo "$yep will be erased. THIS IS UNRECOVERABLE! resume? [Y/n] "
echo ""

read ans

if [ $ans == y ]; then
    echo "Erasing partition table for $yep."
    parted -a optimal -s $yep mklabel msdos
    echo "Done!"
    exit 0
else
    echo "Quitting..."
    exit 0
fi
