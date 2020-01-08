#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Luke Strohm

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

import time
import datetime
from ldap3 import Server, Connection, ALL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


frAddr = 'helpdesk@mlsd.net'
server = smtplib.SMTP(host='relay.mlsd.net', port=25)
today = str(datetime.datetime.today())[:-16]
today2 = datetime.datetime.strptime(today, '%Y-%m-%d')
today3 = today2.strftime('%Y%m%d')
today3 = str(today3+'000000Z')
today4 = today2.strftime('%m/%d/%Y')
one_week = today2 + datetime.timedelta(days=7)
one_week2 = one_week.strftime('%Y%m%d')
one_week2 = str(one_week2+'000000Z')
week_ago = today2 - datetime.timedelta(days=7)
week_ago2 = week_ago.strftime('%Y%m%d')
week_ago2 = str(week_ago2+'000000Z')
# Connect and bind to LDAP server
s = Server('madhs01staff1.mlsd.net', use_ssl=True, get_info=ALL)
c = Connection(s)
c.bind()
# Searches for all active staff accounts with passwords expiring soon
c.search('o=Madison', '(&(objectClass=inetOrgPerson)' +
         '(passwordExpirationTime>='+week_ago2+')' +
         '(passwordExpirationTime<='+one_week2+')(mail=*@mlsd.net)' +
         '(!(loginDisabled=TRUE)))', attributes=['givenName', 'mail', 'uid',
                                                 'passwordExpirationTime',
                                                 'loginGraceRemaining', 'sn'])
users = c.entries
c.unbind()
report = []
for x in users:
    expstr = str(x.passwordExpirationTime.value)[:-15]
    expdate = datetime.datetime.strptime(expstr, '%Y-%m-%d')
    fname = str(x.givenName.value)
    lname = str(x.sn.value)
    uid = str(x.uid.value)
    mail = str(x.mail.value)
    grace = str(x.loginGraceRemaining.value)
    days_remaining = expdate - today2
    days_remaining_str = str(days_remaining)[:-9]
    expStr = expdate.strftime('%m/%d/%Y')  # Pretty date
    msg = MIMEMultipart('alternative')
    msg['From'] = frAddr
    msg['Subject'] = 'Madison Password Expiration Notice '+today4
    msg['To'] = mail
    if today2 > expdate:
        data = str(fname+' '+lname+', username='+uid+', '+mail +
                   ', expiration='+expStr+', '+days_remaining_str[1:]+' ago' +
                   ', grace logins='+grace)
        text = """Hello {fname},
Your Madison OES(Novell) account password for {uid} expired {days_ago} """ +\
"""ago on {expStr}.

You have {grace} grace logins remaining until you are locked out of """ +\
"""your account.

For information on changing your password, please visit the Madison """ +\
"""Tech Office Helpdesk Webpage:

https://helpdesk.mlsd.net/index.php/2018/02/06/change-password/

Thank you,
The Madison Tech Office staff


Raise Expectations, Increase Achievement, Prepare for Tomorrow... """ +\
"""Make it Happen!
"""
        html = """\
<html>
    <body>
        <p>Hello {fname},</p>

        <p>Your Madison OES(Novell) account password for <strong><em>""" +\
"""{uid}</strong></em> expired <strong><em>{days_ago}</strong></em> ago """ +\
"""on <strong><em>{expStr}</strong></em>.</p>

        <p>You have <strong>{grace}</strong> grace logins remaining until """ +\
"""you are locked out of your account.</p>

        <p>For information on changing your password, please visit the """ +\
"""<a href="https://helpdesk.mlsd.net/index.php/2018/02/06/""" +\
"""change-password/">Madison Tech Office Helpdesk Webpage</a>.</p>

        <p>To change your password now, click <a href="https://password.""" +\
"""mlsd.net/sspr/private/login">HERE</a>.</p>

        <p>Thank you,</p>
        <p>The Madison Tech Office staff</p>
        
        <p><em><small>Raise Expectations, Increase Achievement, Prepare """ +\
"""for Tomorrow... Make it Happen!</small></em></p>

        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
    else:
        data = str(fname+' '+lname+', username='+uid+', '+mail +
                   ', expiration='+expStr+', '+days_remaining_str)
        text = """Hello {fname},
This is a courtesy notice to let you know that your Madison OES(Novell)""" +\
""" account password for {uid} will expire in {days_until} on {expStr}.

For information on changing your password, please visit the Madison Tech """ +\
"""Office Helpdesk Webpage:

https://helpdesk.mlsd.net/index.php/2018/02/06/change-password/

Thank you,
The Madison Tech Office staff


Raise Expectations, Increase Achievement, Prepare for Tomorrow... Make """ +\
"""it Happen!
"""
        html = """\
<html>
    <body>
        <p>Hello {fname},</p>

        <p>This is a courtesy notice to let you know that your Madison """ +\
"""OES(Novell) account password for <strong><em>{uid}</strong></em> will """ +\
"""expire in <strong><em>{days_until}</strong></em> on <strong><em>""" +\
"""{expStr}</strong></em>.</p>

        <p>For information on changing your password, please visit the """ +\
"""<a href="https://helpdesk.mlsd.net/index.php/2018/02/06/change-""" +\
"""password/">Madison Tech Office Helpdesk Webpage</a>.</p>

        <p>To change your password now, click <a href="https://password.""" +\
"""mlsd.net/sspr/private/login">HERE</a>.</p>

        <p>Thank you,</p>
        <p>The Madison Tech Office staff</p>

        <p><em><small>Raise Expectations, Increase Achievement, Prepare """ +\
"""for Tomorrow... Make it Happen!</em></small></p>
        
        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    message = msg.as_string()
    server.sendmail(frAddr, mail, message.format(fname=fname, uid=uid,
                                                 days_until=days_remaining_str,
                                                 days_ago=days_remaining_str[1:],
                                                 grace=grace, expStr=expStr))
    report.append(data)

to_addr = ['lstrohm@mlsd.net', 'sbarr@mlsd.net']
msg2 = MIMEMultipart('alternative')
msg2['From'] = frAddr
msg2['Subject'] = 'Password Expiration Report For '+today4
msg2['To'] = ', '.join(to_addr)
text2 = """Hello,

The following users have an upcoming password expiration, or a recently expired password:

""" + '\n'.join(report) + """

Thank you.

Please do not reply to this message.
"""
html2 = """\
<html>
    <body>
        <p>Hello,</p>

        <p>The following users have an upcoming password expiration, or a recently expired password:</p>

        <p>""" + '<br>'.join(report) + """</p>

        <p>Thank you.</p>

        <p><small>Please do not reply to this message.</small></p>
    </body>
</html>
"""
part1a = MIMEText(text2, 'plain')
part2a = MIMEText(html2, 'html')
msg2.attach(part1a)
msg2.attach(part2a)
message2 = msg2.as_string()
server.sendmail(frAddr, 'lstrohm@mlsd.net', message2)
