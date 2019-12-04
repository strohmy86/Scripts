#!/usr/bin/env python3

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

import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    print('\n')
    print(Color.DARKCYAN)
    print("*********************************")
    print("* Python 3 Script For Notifying *")
    print("* Students When an Unauthorized *")
    print("* File Is Found On Their Google *")
    print("*            Drive              *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print(Color.END)


def main():

	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	frAddr = 'noreply@madisonrams.net'
	server = smtplib.SMTP(host='relay.mlsd.net', port=25)
	building = input('What building:  ')
	file = input('What is the filename w/full path:  ')
	with open(file, mode='r') as fh:
		reader = csv.reader(fh)
		next(reader)  # Skip header row
		for email, ids, title, created, mime, modified, owners, name, size in reader:
			print(f'Sending email to '+Color.GREEN+f'{name}'+Color.END)
			msg = MIMEMultipart()
			msg['From'] = frAddr
			msg['Subject'] = 'Unauthorized File Found on Your Google Drive'
			msg['To'] = email

			body = """Hi {name},

A file with the name of "{title}" was discovered during an audit of The Madison Local School District's Google domain.

This file violates MLSD's Acceptible Use Policy that you signed at the beginning of the school year.  The file has been deleted,
and your principal has been notified.  Do not store files of this nature on MLSD's Google Drive in the future.

Continued violations to MLSD's Acceptible Use Policy could result in the loss of your technology privileges.

Thank you for your cooperation,

The Madison Technology Office"""

			msg.attach(MIMEText(body,'plain'))

			text = msg.as_string()
			server.sendmail(
				frAddr,
				email,
				text.format(name=name,title=title),
				)

		with open(building+'-Unauthorized-Files-'+date+'.csv', mode='w', newline='') as fa:
			writer = csv.writer(fa)
			headers = ['Name', 'Email', 'File', 'Created Date', 'Modified Date']
			writer.writerow(headers)
			fs = open(file, mode='r')
			reader2 = csv.reader(fs)
			next(reader2) # Skip header row
			for email, ids, title, created, mime, modified, owners, name, size in reader2:
				data = [name, email, title, created, modified]
				writer.writerow(data)
			fs.close()


cred()
main()
