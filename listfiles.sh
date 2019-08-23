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
	    du -ahc --max-depth=5
	    popd
	done
else
	echo "No directory provided."
fi
