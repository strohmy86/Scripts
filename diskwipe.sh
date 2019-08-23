#!/bin/bash

# MIT License

# Copyright (c) 2019 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
echo "The partition table for $yep will be erased. resume? [Y/n] "
echo ""

read ans

if [[ ($ans == y) || ($ans == Y) || ($ans == "") ]]; then
    echo "Erasing partition table for $yep."
    parted -a optimal -s $yep mklabel msdos
    echo "Done!"
    exit 0
else
    echo "Quitting..."
    exit 0
fi
