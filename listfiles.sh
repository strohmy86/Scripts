#!/bin/bash

echo -n "What is the full directory path you wish to parse?  "

read dir

if [ $dir ]; then
	find $dir/* -type f -print0 | xargs -0 -n1 du -h | sort -n -r
else
	echo "No directory provided."
fi

