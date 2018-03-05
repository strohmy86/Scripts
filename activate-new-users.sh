#!/bin/bash

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
echo "*                               *"
echo "*********************************"

date1=`date --utc +%FT%T.%3NZ --date="7 days ago"`

echo "Getting a list of suspended users..."

gam print users creationtime suspended | grep True | cut -d ',' -f 1-2 > suspended.txt

awk -F'[,]' -v MIN=$date1 '$2 >= MIN' suspended.txt | cut -d ',' -f 1 > susp.txt
sleep 1

echo " Activating suspended users...."

while read i; do
	gam update user $i suspended off
done < susp.txt


echo "Done!"

rm suspended.txt
rm susp.txt
sleep 2

