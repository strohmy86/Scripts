#!/usr/bin/env python3
'''Script to warn students of non-compliant files on their Google Drive'''

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


import argparse
import csv
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Color:
    '''Colors'''
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def cred():
    '''Credentials'''
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "* Python 3 Script For Notifying *\n"
        + "* Students When an Unauthorized *\n"
        + "* File Is Found On Their Google *\n"
        + "*            Drive              *\n"
        + "*                               *\n"
        + "*   Written and maintained by   *\n"
        + "*          Luke Strohm          *\n"
        + "*     strohm.luke@gmail.com     *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*                               *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def main():
    '''Main function'''
    parser = argparse.ArgumentParser(
        description="This is a python script\
                     to send emails to students that have\
                     unauthorized files on their Google Drive."
    )
    parser.add_argument(
        "file",
        metavar="File",
        default="",
        type=str,
        help="CSV file containing unauthorized file info.",
    )
    args = parser.parse_args()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    from_addr = "noreply@madisonrams.net"
    server = smtplib.SMTP(host="relay.mlsd.net", port=25)
    file = args.file
    building = file[14:-13]
    with open(file, mode="r", encoding="UTF-8") as fh:
        reader = csv.reader(fh)
        next(reader)  # Skip header row
        for (email, ids, title, created, mime, modified, owners, name, size,) in reader:
            print("Sending email to " + Color.GREEN + f"{name}" + Color.END)
            msg = MIMEMultipart("alternative")
            msg["From"] = from_addr
            msg["Subject"] = "Unauthorized File Found on Your Google Drive"
            msg["To"] = email
            text = """Hi {name},

A file with the name of "{title}" was discovered during an audit of the
Madison Local School District's Google domain.

This file violates MLSD's Acceptible Use Policy that you signed at the
beginning of the school year.  The file has been deleted,and your principal
has been notified.  Do not store files of this nature on MLSD's Google Drive
in the future.

Continued violations to MLSD's Acceptible Use Policy could result in the loss
of your technology privileges.

Thank you for your cooperation,


The Madison Technology Office"""
            html = """\
<html>
    <body>
        <p>Hi {name},</p>

        <p>A file with the name of <strong><em>{title}</strong></em> was
         discovered during an audit of the Madison Local School District's
         Google domain.</p>

        <p>This file violates MLSD's Acceptible Use Policy that you signed
         at the beginning of the school year.  The file has been deleted,
         and your principal has been notified.  Do not store files of this
         nature on MLSD's Google Drive in the future.</p>

        <p>Continued violations to MLSD's Acceptible Use Policy could result
         in the loss of your technology privileges.</p>

        <p>Thank you for your cooperation,</p>
        <p><br></p>
        <p><em>The Madison Technology Office</em></p>
    </body>
</html>
"""
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            msg.attach(part1)
            msg.attach(part2)
            message = msg.as_string()
            server.sendmail(
                from_addr,
                email,
                message.format(name=name, title=title),
            )
        with open(
            "/home/lstrohm/" + building + "-Unauthorized-Files-" + date + ".csv",
            mode="w", newline="", encoding="UTF-8") as fa:
            writer = csv.writer(fa)
            headers = [
                "Name",
                "Email",
                "File",
                "Created Date",
                "Modified Date",
            ]
            writer.writerow(headers)
            fs = open(file, mode="r", encoding="UTF-8")
            reader2 = csv.reader(fs)
            next(reader2)  # Skip header row
            for (email, ids, title, created, mime, modified, owners, name, size) in reader2:
                data = [name, email, title, created, modified]
                writer.writerow(data)
            fs.close()


cred()
main()
