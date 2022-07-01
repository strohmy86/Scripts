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


import time

from ldap3 import ALL, MODIFY_DELETE, Connection, Server, Tls


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
        + "*  Python 3 Script For Double   *\n"
        + "* Checking that Disabled users  *\n"
        + "*    Are Removed From Groups    *\n"
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
    disabled_ou = "ou=Disabled,ou=Student,ou=Madison,dc=mlsd,dc=local"
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
    c = Connection(s, user=username.strip(), password=password.strip())
    c.bind()
    c.search(
        disabled_ou,
        "(&(objectclass=person)(memberOf=*))",
        attributes=["cn", "memberOf", "title", "physicalDeliveryOfficeName", "department"],
    )
    disabled = c.entries
    for i in disabled:
        print(
            Color.YELLOW
            + "Deleting Groups for account "
            + Color.BOLD
            + str(i.cn.value)
            + Color.END
        )
        if isinstance(i.memberOf.value, list) is True:
            for g in i.memberOf.value:
                c.modify(
                    str(g), {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]}
                )
                time.sleep(0.5)
        elif isinstance(i.memberOf.value, str) is True:
            c.modify(
                i.memberOf.value,
                {"member": [(MODIFY_DELETE, [str(i.entry_dn)])]},
            )
            time.sleep(0.5)
        c.modify(
            str(i.entry_dn),
            {
                "title": [(MODIFY_DELETE, [])],
            },
        )
        time.sleep(0.5)
        c.modify(
            str(i.entry_dn),
            {
                "physicalDeliveryOfficeName": [(MODIFY_DELETE, [])],
            },
        )
        time.sleep(0.5)
        c.modify(
            str(i.entry_dn),
            {
                "department": [(MODIFY_DELETE, [])],
            },
        )
        time.sleep(0.5)
        c.modify(
            str(i.entry_dn),
            {
                "memberOf": [(MODIFY_DELETE, [])],
            },
        )
        time.sleep(0.5)
    time.sleep(1)
    c.unbind()


cred()
main()
