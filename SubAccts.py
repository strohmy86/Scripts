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


import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ldap3 import ALL, MODIFY_REPLACE, Connection, Server, Tls


class Color:
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
    print(Color.DARKCYAN + "\n")
    print("*********************************")
    print("* Python 3 Script For Changing  *")
    print("* Generic Sub Account Passwords *")
    print("*   And Notifying Secretaries   *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print("\n" + Color.END)


def main():
    d = datetime.now().strftime("%m/%d/%y")
    # String of useable characters for the random password
    sx = "abcdefghjkmnopqrstuvwxyz123456789ABCDEFGHJKLMNPQRSTUVWXYZ!@#"
    # Length of random password
    passlen = 8
    # Creates a random password using the allowed characters and length variables
    pw = "".join(random.sample(sx, passlen))

    # LDAP Section, change to suit your environment
    f = open("/home/lstrohm/Scripts/ADcreds.txt", "r")
    lines = f.readlines()
    username = lines[0]
    password = lines[1]
    f.close()
    tls = Tls(
            local_private_key_file=None,
            local_certificate_file=None,
        )
    s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
    c = Connection(s, user=username.strip(),
                password=password.strip())
    c.bind()
    # LDAP search query. Change to suit your needs
    c.search(
        "ou=Madison,dc=mlsd,dc=local",
        "(&(objectclass=person)(cn=*-Sub*))",
        attributes=["fullName", "cn"],
    )
    # Stores query results to a variable.
    subs = c.entries
    # Iterates through the results and changes the account password to the random password generated earlier.
    for i in subs:
        c.extend.microsoft.modify_password(i.entry_dn, pw)
        # print(c.result)
    c.unbind()

    # Email Section

    frAddr = "noreply@madisonrams.net"
    server = smtplib.SMTP(host="relay.mlsd.net", port=25)
    # email = ['lstrohm@mlsd.net',
    #'sbarr@mlsd.net',
    #'mad-mail-secretary@madisonrams.net',
    #'mad-mail-prin@madisonrams.net']
    email = ["lstrohm@mlsd.net"]
    msg = MIMEMultipart("alternative")
    msg["From"] = frAddr
    msg["Subject"] = "Substitute Account Password"
    msg["To"] = ", ".join(email)
    # msg['To'] = email
    text = """Hi,

The new password for all generic sub accounts is:

{pw}

This password is CASE SENSITIVE, and will be active for the week of {d}.



The Madison Technology Office"""

    html = """\
<html>
    <body>
        <p>Hi,</p>

        <p>The new password for all generic sub accounts is <strong><em>
        {pw}</strong></em>.</p>

        <p>This password is <strong>CASE SENSITIVE</strong>, and will be
         active for the week of <strong><mark>{d}</strong></mark>.

        <p>The Madison Technology Office</p>
    </body>
</html>
"""
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    message = msg.as_string()
    server.sendmail(
        frAddr,
        email,
        message.format(pw=pw, d=d),
    )


# cred()
main()
