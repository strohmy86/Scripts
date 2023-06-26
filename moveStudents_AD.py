#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Luke Strohm

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


import datetime
import os
import time

from ldap3 import (
    ALL,
    MODIFY_ADD,
    MODIFY_DELETE,
    MODIFY_REPLACE,
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
        + "*  Python 3 Script For Moving   *\n"
        + "* Disabled Student Accounts in  *\n"
        + "*    LDAP to the Disabled OU    *\n"
        + "*                               *\n"
        + "*   Written and maintained by   *\n"
        + "*          Luke Strohm          *\n"
        + "*     strohm.luke@gmail.com     *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def main():
    f = open("/home/lstrohm/Scripts/ADcreds.txt", "r")
    lines = f.readlines()
    username = lines[0]
    password = lines[1]
    f.close()
    today = str(datetime.datetime.now())
    today2 = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S.%f")
    now = today2.strftime("%m-%d-%Y at %H:%M")
    disabled_ou = "ou="+str(datetime.date.today().year)+",ou=Disabled,ou=Student,ou=Madison,DC=mlsd,DC=local"
    tls = Tls(
        local_private_key_file=None,
        local_certificate_file=None,
    )
    s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
    c = Connection(s, user=username.strip(),
                   password=password.strip())
    c.bind()
    c.search(
        "ou=Active,ou=Student,ou=Madison,DC=mlsd,DC=local",
        "(&(objectclass=person)"
        + "(!(userAccountControl=512))(!(userAccountControl=544))"
        + "(mail=*@madisonrams.net))",
        attributes=["cn", "memberOf"],
    )
    dis = c.entries
    dis_group_dn = [i.memberOf.value for i in dis]
    dis_groups = []
    [dis_groups.append(i) for i in dis_group_dn if i not in dis_groups]
    dis_user_dn = [i.entry_dn for i in dis]
    # print(dis_groups)
    with open("withdrawn.txt", "w", encoding="utf-8") as file:
        for i in dis:
            print(
                Color.YELLOW
                + "Moving account "
                + Color.BOLD
                + str(i.cn.value)
                + Color.END
                + Color.YELLOW
                + " to the disabled student OU."
                + Color.END
            )
            file.write(str(i.entry_dn))
            file.write("\n")
            time.sleep(0.5)
            c.modify(
                str(i.entry_dn),
                {
                    "userAccountControl": [(MODIFY_REPLACE, ["514"])],
                    "description": [
                        (MODIFY_REPLACE, ["Disabled - " + str(now)])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify_dn(
                str(i.entry_dn),
                "cn=" + str(i.cn.value),
                new_superior=disabled_ou,
            )
            cmd = (
                "/home/lstrohm/bin/gamadv-xtd3/gam user "
                + str(i.cn.value)
                + " deprov"
            )
            os.system(cmd)
    file.close()
    for i in dis_groups:
        c.extend.microsoft.remove_members_from_groups([dis_user_dn], i)


    c.unbind()


cred()
main()
