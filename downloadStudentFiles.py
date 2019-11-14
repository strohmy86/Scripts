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
import sys

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def cred():

    print('\n')
    print(Color.DARKCYAN)
    print("*********************************")
    print("*Python 3 Script For Downloading*")
    print("*  Suspicious Files on Student  *")
    print("*         Google Drives         *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print(Color.END)

def download():
    global building
    os.system('export GAM_THREADS=5')
    basedir = '/home/lstrohm/Audit-Files/'+building+'/'
    file = '/home/lstrohm/'+building+'-Filelist.csv'

    with open(file[:-4]+'-Modded.csv', mode='w', newline='') as fa:
        writer = csv.writer(fa)
        headers = ['email', 'id', 'folder']
        writer.writerow(headers)
        fs = open(file, mode='r')
        reader = csv.reader(fs)
        next(reader)  # Skip header row
        for email, ids, title, created, mime, modified, name in reader:
            data = [email, ids, str(basedir+email)]
            writer.writerow(data)
        fs.close()
    fa.close()

    cmd = '/home/lstrohm/bin/gam/gam csv /home/lstrohm/'+building+'-Filelist-Modded.csv gam user ~email get drivefile id ~id targetfolder ~folder format microsoft'
    os.system(cmd)
    os.system('export GAM_THREADS=15')

def makeCsv():
    global building
    query = 'query "mimeType contains *java* OR mimeType contains *download* OR mimeType contains *zip* OR mimeType contains *audio/* OR mimeType contains *image/* OR mimeType contains *video/*"'
    query1 = query.replace("*", r"'")
    cmd = '/home/lstrohm/bin/gam/gam ou "/Student/' +building+ '" show filelist ' +query1+ ' id name createddate mimetype modifieddate ownerNames > /home/lstrohm/'+building+'-Filelist.csv'
    os.system(cmd)
    file = '/home/lstrohm/'+building+'-Filelist.csv'
    print('\n')
    print(Color.YELLOW+'File saved as '+building+'-Filelist.csv in "/home/lstrohm/"\n'+Color.END)

cred()
building = input(Color.BOLD+'What is the building:  '+Color.END)
makeCsv()
download()

sys.exit()
