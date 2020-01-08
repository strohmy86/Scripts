#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

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
import argparse
import datetime


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
    print(Color.DARKCYAN + '\n')
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
    print('\n' + Color.END)


def download(building):
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
        power_labels = {0: '', 1: 'Kilo', 2: 'Mega', 3: 'Giga', 4: 'Tera'}
        for email, ids, title, created, mime, modified, owners, name, size\
                in reader:
            data = [email, ids, str(basedir+email)]
            writer.writerow(data)
            if size in (None, ""):
                continue
            total += int(size)
        fs.close()
    fa.close()
    cmd = '/home/lstrohm/bin/gamadv-xtd3/gam config num_threads = 5 csv \
        /home/lstrohm/'+building+'-Filelist-Modded.csv gam user ~email \
        get drivefile id ~id targetfolder ~folder format microsoft'
    power = 2**10
    n = 0
    while total > power:
        total /= power
        n += 1
    total = format(total, '.2f')  # give 2 digits after the point
    sel = input(Color.RED + str(total) + ' ' + power_labels[n] +
                'bytes is going to be downloaded. Do you wish to continue? ' +
                '[Y/n]  '+Color.END)
    if sel == 'y' or sel == 'Y' or sel == 'yes' or sel == 'Yes' or\
            sel == 'YES' or sel == '':  # If yes, the function continues
        os.system(cmd)
    elif sel == 'n' or sel == 'N' or sel == 'no' or sel == 'No' or\
            sel == 'NO':  # If no, the program exits
        exit()
    else:  # If yes or no is not given, the script errors out and exits
        print(Color.RED + 'Error!' + Color.END)
        time.sleep(1)
        exit()


def makeCsv(building):
    now = time.localtime()
    # Get the last day of last month by taking the first day of this month
    # and subtracting 1 day.
    last = datetime.date(now.tm_year, now.tm_mon, 1) - \
        datetime.timedelta(days=1)
    last2 = last.strftime('%Y-%m-%d')
    # Set the day to 1 gives us the start of last month
    first = last.replace(day=1)
    first2 = first.strftime('%Y-%m-%d')
    first = str(first2+'T00:00:00')  # Format that Google recognizes
    last = str(last2+'T00:00:00')  # Format that Google recognizes
    query = 'query "not mimeType contains *vnd.google* and mimeType!=' +\
        '*text/plain* and not mimeType contains *officedocument* ' +\
        'and not name contains *Getting Started* and trashed!=True ' +\
        'and not name contains *.hex* and mimeType!=*application/' +\
        'msword* and mimeType!=*application/pdf* and (modifiedTime > *' +\
        first+'* or createdTime > *'+first+'*) and (modifiedTime < *' +\
        last+'* or createdTime < *'+last+'*)"'
    query1 = query.replace("*", r"'")
    cmd = '/home/lstrohm/bin/gamadv-xtd3/gam redirect csv /home/lstrohm/' +\
        building+'-Filelist.csv multiprocess ou "/Student/'+building +\
        '" print filelist '+query1+' fields id,name,createdtime,mimetype,' +\
        'modifiedtime,owners.displayname,size'
    os.system(cmd)
    file = '/home/lstrohm/'+building+'-Filelist.csv'
    print(Color.YELLOW+'\nFile saved as '+file+'\n'+Color.END)


parser = argparse.ArgumentParser(description='Script to search for and\
                                download suspicious files on student\
                                Google Drives')
parser.add_argument('bldg', metavar='Building', default='',
                    type=str, help='2 digit building code')
args = parser.parse_args()
building = args.bldg


cred()
makeCsv(building)
download(building)
