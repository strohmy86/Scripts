#!/bin/bash

if [ "$1" == "" ]
then
echo "Usage: ./pingsweep.sh [network segment]"
echo "Example: ./pingsweep.sh 192.168.1"
else
for x in `seq 1 254`; do
	ping -c 1 $1.$x | grep "64 bytes" | cut -d " " -f 4 | sed 's/.$//'
done
fi


