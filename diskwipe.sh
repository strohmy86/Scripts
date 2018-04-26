#!/bin/bash

dev="/dev/"
disk=$(lsblk | grep disk  | awk '{print $1}' | sort | head -n 1)
yep=$dev$disk

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

echo "$yep will be erased. THIS IS UNRECOVERABLE! resume? [Y/n] "
echo ""

read ans

if [ $ans == y ]; then
    echo "Erasing partition tatble for $yep."
    parted -a optimal -s $yep mklabel msdos
    echo "Done!"
else
    echo "Quitting..."
fi
