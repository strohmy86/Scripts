#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

echo ""
echo "*********************************"
echo "*  Directory Listing Utility    *"
echo "*                               *"
echo "*  Written and maintained by:   *"
echo "*        Luke Strohm            *"
echo "*    strohm.luke@gmail.com      *"
echo "*                               *"
echo "*********************************"
echo ""

echo "What is the full directory path you wish to parse?"
echo ""

read dir

if [ ${dir} ]; then
	find ${dir} -mindepth 1 -maxdepth 1 -type d | while read -r dir
	do
	    pushd "$dir"
	    echo ${bold}${dir}${normal}
	    du -shc
	    popd
	done
else
	echo "No directory provided."
fi

