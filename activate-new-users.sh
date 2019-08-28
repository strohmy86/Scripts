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

PATH="$PATH:~/bin/gam"; export PATH

echo "*********************************"
echo "*  GAM script to activate new   *"
echo "*  users that are suspended at  *"
echo "*     creation time by GCDS.    *"
echo "*                               *"
echo "*     Uses  GAM by jay0lee      *"
echo "*                               *"
echo "*   Written and maintained by:  *"
echo "*         Luke Strohm           *"
echo "*    strohm.luke@gmail.com      *"
echo "*  https://github.com/strohmy86 *"
echo "*                               *"
echo "*********************************"

date1=`date --utc +%FT%T.%3NZ --date="7 days ago"`

echo "Getting a list of suspended users..."

gam print users creationtime suspended | grep True | cut -d ',' -f 1-2 > suspended.txt

awk -F'[,]' -v MIN=${date1} '$2 >= MIN' suspended.txt | cut -d ',' -f 1 > susp.txt
sleep 1

echo " Activating suspended users...."

while read i; do
	gam update user ${i} suspended off
done < susp.txt


echo "Done!"

rm suspended.txt
rm susp.txt
sleep 2
