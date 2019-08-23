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
