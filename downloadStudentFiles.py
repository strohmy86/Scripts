#!/bin/env python3

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

import os
import csv

building = input('What is the building:  ')
file = input('What is the file:  ')
basedir = '/home/lstrohm/Audit-Files/'+building+'/'

with open(file) as csvfile:
    readcsv = csv.reader(csvfile)
    next(readcsv)
    for email in readcsv:
        #print(str(email)[2:-2])
        output = basedir+str(email)[2:-2]
        user = str(email)[2:-2]
        if os.path.isdir(output) == False:
            os.mkdir(output)

        query = 'query "mimeType contains *java* OR mimeType contains *download* OR mimeType contains *zip* OR mimeType contains *audio/* OR mimeType contains *image/* OR mimeType contains *video/*"'
        query1 = query.replace("*", r"'")
        cmd = '/home/lstrohm/bin/gam/gam user ' +user+' get drivefile ' + query1 + ' targetfolder ' + output + ' format microsoft'
        os.system(cmd)
csvfile.close()
