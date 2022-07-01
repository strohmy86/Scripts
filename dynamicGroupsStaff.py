#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and assoc      'ocumentation files (the "Software\n' +, to deal
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

import time

import paramiko
from ldap3 import (
    ALL,
    MODIFY_ADD,
    MODIFY_DELETE,
    Connection,
    Server,
    Tls,
)

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
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "*      Python 3 Script For      *\n"
        + "* Maintaining Dynamic Groups in *\n"
        + "*        Active Directory       *\n"
        + "*                               *\n"
        + "*   Written and maintained by   *\n"
        + "*          Luke Strohm          *\n"
        + "*     strohm.luke@gmail.com     *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )

## Connection and Global variables
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
# Specify private key file
k = paramiko.RSAKey.from_private_key_file("/home/lstrohm/.ssh/id_rsa")
# Connects to gcds server via SSH
gcds = paramiko.SSHClient()
gcds.set_missing_host_key_policy(paramiko.AutoAddPolicy())
gcds.connect("madhs01gcds.mlsd.local", username="mlsd\\administrator", pkey=k)

c.search(
    "ou=Madison,DC=mlsd,DC=local",
    "(&(|(mail=*@mlsd.net)(mail=*@madisonadultcc.org))(objectClass=person))",
    attributes=["cn", "memberOf", "department","physicalDeliveryOfficeName",
     "userAccountControl", "title",],
)
users = c.entries



def main(c, gcds, users):
    #------------------------------911-Notify------------------------------#
    for i in users:
        if "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "911".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "911".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to 911-notify"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("911".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from 911-notify"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )
    

    #------------------------------cabinet------------------------------#
    for i in users:
        if "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Cabinet".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Cabinet".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to cabinet"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Cabinet".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from cabinet"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------certified------------------------------#
    for i in users:
        if "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "CERT".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "CERT".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to certified"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("CERT".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from certified"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------classified------------------------------#
    for i in users:
        if "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "CLSFD".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "CLSFD".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to classified"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("CLSFD".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from classified"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )
    

    #------------------------------mad-mail-1------------------------------#
    for i in users:
        if "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "1st".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "1st".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-1"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("1st".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-1"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-2------------------------------#
    for i in users:
        if "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "2nd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "2nd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-2"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("2nd".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-2"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-3------------------------------#
    for i in users:
        if "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "3rd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "3rd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-3"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("3rd".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-3"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-4------------------------------#
    for i in users:
        if "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "4th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "4th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-4"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("4th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-4"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-5------------------------------#
    for i in users:
        if "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "5th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "5th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-5"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("5th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-5"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-6------------------------------#
    for i in users:
        if "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "6th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "6th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-6"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("6th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-6"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-k------------------------------#
    for i in users:
        if "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "k".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "k".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-k"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("k".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-k"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-admin------------------------------#
    for i in users:
        if "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "adminteam".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "adminteam".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-admin"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("adminteam".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-admin"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-custodian------------------------------#
    for i in users:
        if "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("custodian".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-foodsvc------------------------------#
    for i in users:
        if "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-foodsvc"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("cook".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-foodsvc"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-guidance------------------------------#
    for i in users:
        if "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "guidance".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "guidance".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-guidance"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("guidance".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-guidance"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-nurse------------------------------#
    for i in users:
        if "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "nurse".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "nurse".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-nurse"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("nurse".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-nurse"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-para------------------------------#
    for i in users:
        if "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("para".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-pe------------------------------#
    for i in users:
        if "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "physed".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "physed".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-pe"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("physed".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-pe"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-pltw------------------------------#
    for i in users:
        if "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "pltw".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "pltw".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-pltw"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("pltw".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-pltw"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-prin------------------------------#
    for i in users:
        if "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "principal".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "principal".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-prin"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("principal".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-prin"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-secretary------------------------------#
    for i in users:
        if "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "secretary".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "secretary".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-secretary"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("secretary".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-secretary"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-sis------------------------------#
    for i in users:
        if "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "sis".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "sis".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-sis"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("sis".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-sis"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-sped------------------------------#
    for i in users:
        if "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "intervention".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "intervention".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-sped"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("intervention".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-sped"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-teacher------------------------------#
    for i in users:
        if "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-title1------------------------------#
    for i in users:
        if "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "title 1".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "title 1".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-title1"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("title 1".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-title1"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-user------------------------------#
    for i in users:
        if "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "sub".lower() not in str(i.cn.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "sub".lower() not in str(i.cn.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "514" in str(i.userAccountControl.value):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-tech------------------------------#
    for i in users:
        if "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-tech"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-tech"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad56-mail-teacher------------------------------#
    for i in users:
        if "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "56".lower() in \
        str(i.department.value).lower() and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "56".lower() in \
        str(i.department.value).lower() and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad56-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "56".lower() not in \
        str(i.department.value).lower()) or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad56-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad78-mail-teacher------------------------------#
    for i in users:
        if "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "78".lower() in \
        str(i.department.value).lower() and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "78".lower() in \
        str(i.department.value).lower() and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad78-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "78".lower() not in \
        str(i.department.value).lower()) or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad78-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad56-mail-user------------------------------#
    for i in users:
        if "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "56".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "56".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad56-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("56".lower() not in str(i.department.value).lower() or "514" \
        in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad56-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad78-mail-user------------------------------#
    for i in users:
        if "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "78".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "78".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad78-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("78".lower() not in str(i.department.value).lower() or "514" \
        in str(i.userAccountControl.value)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad78-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madea-mail-custodian------------------------------#
    for i in users:
        if "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madea-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madmi-mail-custodian------------------------------#
    for i in users:
        if "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madso-mail-custodian------------------------------#
    for i in users:
        if "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madso-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "south".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-mail-custodian------------------------------#
    for i in users:
        if "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-mail-custodian------------------------------#
    for i in users:
        if "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-custodian"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "high".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-custodian"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madea-mail-para------------------------------#
    for i in users:
        if "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madea-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madmi-mail-para------------------------------#
    for i in users:
        if "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madso-mail-para------------------------------#
    for i in users:
        if "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madso-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "south".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-mail-para------------------------------#
    for i in users:
        if "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-mail-para------------------------------#
    for i in users:
        if "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-para"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "high".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-para"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madea-mail-teacher------------------------------#
    for i in users:
        if "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madea-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madmi-mail-teacher------------------------------#
    for i in users:
        if "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or \
        "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madso-mail-teacher------------------------------#
    for i in users:
        if "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madso-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or \
        "south".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-mail-teacher------------------------------#
    for i in users:
        if "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or \
        "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-mail-teacher------------------------------#
    for i in users:
        if "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-teacher"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or \
        "high".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-teacher"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madea-mail-user------------------------------#
    for i in users:
        if "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madea-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madmi-mail-user------------------------------#
    for i in users:
        if "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madso-mail-user------------------------------#
    for i in users:
        if "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "south".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "south".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madso-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("south".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-mail-user------------------------------#
    for i in users:
        if "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("middle".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-mail-user------------------------------#
    for i in users:
        if "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "high".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "high".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("high".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madjb-mail-user------------------------------#
    for i in users:
        if "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "early childhood".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "early childhood".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madjb-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("early childhood".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madjb-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madea-mail-cook------------------------------#
    for i in users:
        if "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madea-mail-cook"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-cook"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madmi-mail-cook------------------------------#
    for i in users:
        if "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-cook"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-cook"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madso-mail-cook------------------------------#
    for i in users:
        if "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "south".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madso-mail-cook"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "south".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-cook"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-mail-cook------------------------------#
    for i in users:
        if "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-mail-cook"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-cook"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-mail-cook------------------------------#
    for i in users:
        if "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-cook"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "high".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-cook"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madms-halo------------------------------#
    for i in users:
        if "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madms-halo"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("halo".lower() not in str(i.department.value).lower() or \
        "middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madms-halo"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madhs-halo------------------------------#
    for i in users:
        if "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madhs-halo"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("halo".lower() not in str(i.department.value).lower() or \
        "high".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madhs-halo"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mlea------------------------------#
    for i in users:
        if "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "mlea".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "mlea".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mlea"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("mlea".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mlea"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------oapse------------------------------#
    for i in users:
        if "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "oapse".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "oapse".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to oapse"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("oapse".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from oapse"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------slo-trainers------------------------------#
    for i in users:
        if "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "SLO".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "SLO".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to slo-trainers"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("SLO".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from slo-trainers"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------titleixcoordinator------------------------------#
    for i in users:
        if "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Title IX".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            continue
        elif "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Title IX".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to titleixcoordinator"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Title IX".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from titleixcoordinator"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------Helpdesk------------------------------#
    for i in users:
        if "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to Helpdesk"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from Helpdesk"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-emis------------------------------#
    for i in users:
        if "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "EMIS".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "EMIS".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-emis"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("EMIS".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-emis"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-ps------------------------------#
    for i in users:
        if "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Preschool".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Preschool".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-ps"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Preschool".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-ps"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------mad-mail-tech------------------------------#
    for i in users:
        if "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to mad-mail-tech"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from mad-mail-tech"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madbo-mail-user------------------------------#
    for i in users:
        if "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Administration Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Administration Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madbo-mail-user"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Administration Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madbo-mail-user"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )


    #------------------------------madelem-mail-sped------------------------------#
    for i in users:
        if "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "Inervention".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            continue
        elif "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Inervention".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.CYAN
            + " to madelem-mail-sped"
            + Color.END
            )   
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(i.entry_dn)])],
                },
            )
        elif "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Inervention".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
            + Color.YELLOW
            + " from madelem-mail-sped"
            + Color.END
            )
            c.modify(
            str(i.entry_dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
                )

    c.unbind()

    # Connects to madhs01gcds server via SSH and runs a Google Sync
    stdin, stdout, stderr = gcds.exec_command("C:\Tools\gcds.cmd")
    for line in stdout:
        print(Color.YELLOW + line.strip("\n") + Color.END)

    

cred()
main(c, gcds, users)
