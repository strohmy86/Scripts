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
import time

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
    basedir = '/home/lstrohm/Audit-Files/'+building+'/'
    file = '/home/lstrohm/'+building+'-Filelist.csv'

    with open(file[:-4]+'-Modded.csv', mode='w', newline='') as fa:
        writer = csv.writer(fa)
        headers = ['email', 'id', 'folder']
        writer.writerow(headers)
        fs = open(file, mode='r')
        reader = csv.reader(fs)
        next(reader)  # Skip header row
        total = 0
        power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
        for email, ids, title, created, mime, modified, owners, name, size in reader:
            data = [email, ids, str(basedir+email)]
            writer.writerow(data)
            total += size
        fs.close()
    fa.close()

    cmd = '/home/lstrohm/bin/gamadv-xtd3/gam config num_threads = 5 csv /home/lstrohm/'+building+'-Filelist-Modded.csv gam user ~email get drivefile id ~id targetfolder ~folder format microsoft'
    power = 2**10
    n = 0
    while total > power:
        total /= power
        n += 1
    total = format(total, '.2f') # give 2 digits after the point

    sel = input(Color.RED + str(total) + ' ' + power_labels[n]+'bytes is going to be downloaded. Do you wish to continue? [Y/n]  ' + Color.END)
    if sel =='y' or sel == 'Y' or sel == 'yes' or sel == 'Yes' or sel == 'YES' or sel == '': # If yes, the function continues
        os.system(cmd)
    elif sel =='n' or sel == 'N' or sel == 'no' or sel == 'No' or sel == 'NO': # If no, the program exits
        exit()
    else: # If anything other than an input above is given, the script errors out and exits
        print(Color.RED + 'Error!' + Color.END)
        time.sleep(1)
        exit()

def makeCsv():
    global building
    query = 'query "not mimeType contains *vnd.google* and mimeType!=*text/plain* and not mimeType contains *officedocument* and not name contains *Getting Started* and trashed!=True"'
    query1 = query.replace("*", r"'")
    cmd = '/home/lstrohm/bin/gamadv-xtd3/gam redirect csv /home/lstrohm/'+building+'-Filelist.csv multiprocess ou "/Student/' +building+ '" print filelist ' +query1+' fields id,name,createdtime,mimetype,modifiedtime,owners.displayname,size'
    os.system(cmd)
    file = '/home/lstrohm/'+building+'-Filelist.csv'
    print('\n')
    print(Color.YELLOW+'File saved as '+file+'\n'+Color.END)

cred()
building = input(Color.BOLD+'What is the building:  '+Color.END)
makeCsv()
download()

exit()
