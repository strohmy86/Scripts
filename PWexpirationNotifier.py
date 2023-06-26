#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This script is designed to be run automatically, so no pretty text display.

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ldap3 import ALL, Connection, Server, Tls


# Constant Variables
frAddr = "helpdesk@mlsd.net"
server = smtplib.SMTP(host="relay.mlsd.net", port=25)
today = str(datetime.datetime.today())[:-16]
today2 = datetime.datetime.strptime(today, "%Y-%m-%d")
today3 = today2.strftime("%Y%m%d")
today3 = str(today3 + "000000Z")
today4 = today2.strftime("%m/%d/%Y")
one_week = today2 + datetime.timedelta(days=7)
one_week2 = one_week.strftime("%Y%m%d")
week_ago = today2 - datetime.timedelta(days=7)
week_ago2 = week_ago.strftime("%Y%m%d")

# Connect and bind to LDAP server
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
# Searches for all active staff accounts with passwords expiring soon
c.search(
    "ou=Madison,dc=mlsd,dc=local",
    "(&(objectClass=person)"
    + "(|(mail=*@mlsd.net)(mail=*@madisonadultcc.org))"
    + "(!(userAccountControl=514))(!(userAccountcontrol=546))"
    + "(!(pwdLastSet=0)))",
    attributes=[
        "givenName",
        "mail",
        "cn",
        "pwdLastSet",
        "sn",
    ],
)
users = c.entries
c.unbind()
report = []

for x in users:
    setstr = str(x.pwdLastSet.value)[:-22]
    setdate = datetime.datetime.strptime(setstr, "%Y-%m-%d")
    expdate = setdate + datetime.timedelta(days=90)
    fname = str(x.givenName.value)
    lname = str(x.sn.value)
    cn = str(x.cn.value)
    mail = str(x.mail.value)
    days_remaining = expdate - today2
    days_remaining_str = str(days_remaining)[:-9]
    days_ago = days_remaining_str[1:]
    expStr = expdate.strftime("%m/%d/%Y")  # Pretty date
    msg = MIMEMultipart("alternative")
    msg["From"] = frAddr
    msg["Subject"] = "Madison Password Expiration Notice " + today4
    msg["To"] = mail
    if today2 > expdate and int(days_remaining.days) >= -14:
        data = str(
            fname
            + " "
            + lname
            + ", username="
            + cn
            + ", "
            + mail
            + ", expiration="
            + expStr
            + ", "
            + days_ago
            + " ago"
        )
        text = (
            """Hello {fname},
Your Madison Active Directory account password for {cn} expired {days_ago} """
            + """ago on {expStr}.

For information on changing your password, please visit the Madison """
            + """Tech Office Helpdesk Webpage:

https://helpdesk.mlsd.net/index.php/2018/02/06/change-password/

Thank you,
The Madison Tech Office staff
"""
        )
        html = (
            """\
<html>
    <body>
        <p>Hello {fname},</p>

        <p>Your Madison Active Directory account password for <strong><em>"""
            + """{cn}</strong></em> expired <strong><em>{days_ago}"""
            + """</strong></em> ago on <strong><em>{expStr}</strong></em>.</p>

        <p>For information on changing your password, please visit the """
            + """<a href="https://helpdesk.mlsd.net/index.php/2018/02/06/"""
            + """change-password/">Madison Tech Office Helpdesk Webpage</a>.</p>

        <p>To change your password now, click <a href="https://pwd."""
            + """mlsd.net">HERE</a>.</p>

        <p>Thank you,</p>
        <p>The Madison Tech Office staff</p>


        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
        )
    elif today2 < expdate and int(days_remaining.days)  <= 7 and int(days_remaining.days) >= 1:
        data = str(
            fname
            + " "
            + lname
            + ", username="
            + cn
            + ", "
            + mail
            + ", expiration="
            + expStr
            + ", "
            + days_remaining_str
        )
        text = (
            """Hello {fname},
This is a courtesy notice to let you know that your Madison Active Directory"""
            + """ account password for {cn} will expire in {days_until}"""
            + """ on {expStr}.

For information on changing your password, please visit the Madison Tech"""
            + """ Office Helpdesk Webpage:

https://helpdesk.mlsd.net/index.php/2018/02/06/change-password/

Thank you,
The Madison Tech Office staff
"""
        )
        html = (
            """\
<html>
    <body>
        <p>Hello {fname},</p>

        <p>This is a courtesy notice to let you know that your Madison """
            + """Active Directory account password for <strong><em>{cn}"""
            + """</strong></em> will expire in <strong><em>{days_until}"""
            + """</strong></em> on <strong><em>{expStr}</strong></em>.</p>

        <p>For information on changing your password, please visit the """
            + """<a href="https://helpdesk.mlsd.net/index.php/2018/02/06"""
            + """/change-password/">Madison Tech Office Helpdesk Webpage</a>.</p>

        <p>To change your password now, click <a href="https://pwd."""
            + """mlsd.net">HERE</a>.</p>

        <p>Thank you,</p>
        <p>The Madison Tech Office staff</p>

        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
        )

    else:
        continue

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    message = msg.as_string()
    server.sendmail(
        frAddr,
        mail,
        message.format(
            fname=fname,
            cn=cn,
            days_until=days_remaining_str,
            days_ago=days_ago,
            expStr=expStr,
        ),
    )
    report.append(data)

to_addr = ["lstrohm@mlsd.net", "cmcvicker@mlsd.net"]
msg2 = MIMEMultipart("alternative")
msg2["From"] = frAddr
msg2["Subject"] = "Password Expiration Report For " + today4
msg2["To"] = ", ".join(to_addr)
text2 = (
    """Hello,

The following users have an upcoming password expiration, or a recently """
    + """expired password:

"""
    + "\n".join(report)
    + """

Thank you.

Please do not reply to this message.
"""
)
html2 = (
    """\
<html>
    <body>
        <p>Hello,</p>

        <p>The following users have an upcoming password expiration, or """
    + """a recently expired password:</p>

        <p>"""
    + "<br>".join(report)
    + """</p>

        <p>Thank you.</p>

        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
)
part1a = MIMEText(text2, "plain")
part2a = MIMEText(html2, "html")
msg2.attach(part1a)
msg2.attach(part2a)
message2 = msg2.as_string()
server.sendmail(frAddr, to_addr, message2)
