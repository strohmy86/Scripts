#!/bin/bash

PATH="$PATH:~/bin/gam"; export PATH

echo "*********************************"
echo "*  GAM script to activate the   *"
echo "*    Enroll user that gets      *"
echo "*   suspended periodically.     *"
echo "*                               *"
echo "*     Uses  GAM by jay0lee      *"
echo "*                               *"
echo "*   Written and maintained by:  *"
echo "*         Luke Strohm           *"
echo "*    strohm.luke@gmail.com      *"
echo "*                               *"
echo "*********************************"

echo "Checking status of Enroll user..."
gam info user enroll | grep Suspended > enroll.txt
sleep 2

if grep -q True "enroll.txt"; then
	echo "Enroll user is suspended. Activating user..."
	gam update user enroll suspended off
	echo "Done."
	sleep 1 
	echo "Double checking Enroll user status..."
	gam info user enroll | grep Suspended > enroll.txt
	if grep -q True "enroll.txt"; then
		echo "Enroll user is still suspended. Try manually activating."
	else
		echo "Enroll user is activated!"
	fi
else
	echo "Enroll user is not suspended."
fi

rm enroll.txt

