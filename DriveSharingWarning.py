#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Luke Strohm

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


import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import argparse


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
    print(Color.DARKCYAN+'\n' +
          '*********************************\n' +
          '* Python 3 Script For Notifying *\n' +
          '*   Users When a Drive File is  *\n' +
          '*       Shared With Anyone      *\n' +
          '*                               *\n' +
          '*   Written and maintained by   *\n' +
          '*          Luke Strohm          *\n' +
          '*     strohm.luke@gmail.com     *\n' +
          '*  https://github.com/strohmy86 *\n' +
          '*                               *\n' +
          '*********************************\n' +
          '\n'+Color.END)


def main():
    parser = argparse.ArgumentParser(description='This is a python script to\
                                     send emails to users that have a file\
                                     shared with anyone.')
    parser.add_argument('file', metavar='File', default='',
                        type=str, help='CSV file containing Drive file info.')
    args = parser.parse_args()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    frAddr = 'noreply@madisonrams.net'
    server = smtplib.SMTP(host='relay.mlsd.net', port=25)
    file = args.file
    with open(file, mode='r') as fh:
        reader = csv.reader(fh)
        next(reader)  # Skip header row
        for email, ids, title, permissionid, role, discoverable in reader:
            if permissionid == 'id:anyone':
                permission = 'anyone'
                explanation = 'everyone in the world has access to the file'
            elif permissionid == 'id:anyoneWithLink':
                permission = 'anyone with the link'
                explanation = 'everyone in the world with the link has ' +\
                            'access to the file'
            if role == 'writer':
                edit = ', and can edit said file'
            else:
                edit = ''
            print(f'Sending email to '+Color.GREEN+f'{email}'+Color.END)
            msg = MIMEMultipart('alternative')
            msg['From'] = frAddr
            msg['Subject']='Risky Sharing Settings Found on your Google Drive'
            msg['To'] = email
            text = """Hello,

A file with the name of "{title}" was discovered during a file sharing audit 
of the Madison Local School District's Google domain.

The permission on this file is set to "{permission}", 
with the role of "{role}".

This means that {explanation}{edit}.

This can possibly be a great security risk, depending on the content of the file.
It is STRONGLY suggested that this be changed to specific users, groups, 
or limited to within the domain of madisonrams.net

For instructions on changing file sharing permissions, see the following link:
https://support.google.com/docs/answer/2494893

Thank you for your cooperation,


The Madison Technology Office"""
            html = """\
<html>
    <body>
        <p>Hello,</p>

        <p>A file with the name of <strong><em>{title}</strong></em> was
         discovered during a file sharing audit of the Madison Local School
         District's Google domain.</p>

        <p>The permission on this file is set to <strong><em>{permission}
        </strong></em> with the role of <strong><em>{role}</strong></em>, 
        meaning that <strong><em>{explanation}{edit}.</strong></em></p>


        <p>This can possibly be a great security risk, depending on the 
        content of the file. It is <strong>strongly</strong> suggested 
        that this be changed to specific users, groups, or limited to 
        within the domain of madisonrams.net</p>

        <p> Click <a href="https://support.google.com/docs/answer/2494893">
        HERE</a> for instructions on changing file sharing permissions.</p>

        <p>Thank you for your cooperation,</p>
        <p><br></p>
        <p><em>The Madison Technology Office</em></p>
    </body>
</html>
"""
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            message = msg.as_string()
            server.sendmail(
                frAddr,
                email,
                message.format(title=title, permission=permission, role=role,
                               explanation=explanation, edit=edit),
                )
    fh.close()
    with open('/home/lstrohm/DriveSharingAudit-'+date+'.csv', mode='w',
              newline='') as fa:
        writer = csv.writer(fa)
        headers = ['Email', 'File', 'Permission', 'Role', 'Discoverable']
        writer.writerow(headers)
        fs = open(file, mode='r')
        reader2 = csv.reader(fs)
        next(reader2)  # Skip header row
        for email, ids, title, permissionid, role, discoverable in reader2:
            if permissionid == 'id:anyone':
                permission = 'Anyone'
            elif permissionid == 'id:anyoneWithLink':
                permission = 'Anyone with the link'
            data = [email, title, permission, role, discoverable]
            writer.writerow(data)
        fs.close()
    fa.close()


cred()
main()
