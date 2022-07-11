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

from ldap3 import (
    ALL,
    MODIFY_ADD,
    MODIFY_DELETE,
    SUBTREE,
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

def main():
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
    
    users = c.extend.standard.paged_search(search_base="ou=Madison,DC=mlsd,DC=local",
        search_filter="(&(mail=*madisonrams.net)(objectClass=person))",
        search_scope=SUBTREE, attributes=["cn", "memberOf", "description", 
        "physicalDeliveryOfficeName", "userAccountControl", "title",],
        paged_size=5, generator=False
    )


    #------------------------------mad-student-inet------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-inet,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("514" not in str(status) or "546" not in str(status)):
            continue
        elif "CN=mad-student-inet,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and ("514" not in str(status) or "546" not in str(status)):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-inet"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-inet,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-inet,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-inet,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-inet"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-k------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "KG".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "KG".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-k"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("KG".lower() not in str(description).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-k"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-1------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "01".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "01".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-1"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("01".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-1"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-2------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "02".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "02".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-2"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("02".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-2"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-3------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "03".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "03".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-3"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("03".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-3"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-4------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "04".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "04".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-4"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("04".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-4"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-5------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "05".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "05".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-5"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("05".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-5"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-5,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-6------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "06".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "06".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-6"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("06".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-6"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-6,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-7------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "07".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "07".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-7"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("07".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-7"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-7,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-8------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "08".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "08".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-8"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("08".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-8"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-8,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-9------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "09".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "09".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-9"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("09".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-9"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-9,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-10------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "10".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "10".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-10"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("10".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-10"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-10,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-11------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "11".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "11".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-11"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("11".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-11"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-11,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-12------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "12".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "12".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-12"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("12".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-12"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-12,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-ct------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "CT".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "CT".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-ct"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("CT".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-ct"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-ct,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-ct10------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "CT".lower() in str(description).lower() and "10".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "CT".lower() in str(description).lower() and "10".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-ct10"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("CT".lower() not in str(description).lower() and \
        "10".lower() in str(description).lower()) or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-ct10"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-ct10,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-ct11------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "CT".lower() in str(description).lower() and "11".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "CT".lower() in str(description).lower() and "11".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-ct11"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("CT".lower() not in str(description).lower() and \
        "11".lower() in str(description).lower()) or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-ct11"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-ct11,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------mad-student-ct12------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "CT".lower() in str(description).lower() and "12".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "CT".lower() in str(description).lower() and "12".lower() \
        in str(description).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to mad-student-ct12"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("CT".lower() not in str(description).lower() and \
        "12".lower() in str(description).lower()) or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from mad-student-ct12"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=mad-student-ct12,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-cosmetology------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Cosmetology".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Cosmetology".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-cosmetology"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Cosmetology".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-cosmetology"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-cosmetology,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-dental-assisting------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Dental Assisting".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Dental Assisting".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-dental-assisting"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Dental Assisting".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-dental-assisting"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-dental-assisting,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-elec-maint------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Electrical Maintenance".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Electrical Maintenance".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-elec-maint"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Electrical Maintenance".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-elec-maint"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-elec-maint,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-med-asst------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Medical Assisting".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Medical Assisting".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-med-asst"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Medical Assisting".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-med-asst"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-med-asst,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-med-legal-ofc-mgmt------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Medical & Legal Office Management".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Medical & Legal Office Management".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-med-legal-ofc-mgmt"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Medical & Legal Office Management".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-med-legal-ofc-mgmt"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-med-legal-ofc-mgmt,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-premach------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Precision Machining".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Precision Machining".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-premach"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Precision Machining".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-premach"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-premach,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madae-student-welding------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Welding Technology".lower() in str(description).lower() and "514" not in \
        str(status):
            continue
        elif "CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Welding Technology".lower() in str(description).lower() and "514" not in \
        str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madae-student-welding"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Welding Technology".lower() not in str(description).lower() or "514" in \
        str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madae-student-welding"
            + Color.END
            )
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_DELETE, ["CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madae-student-welding,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-student-k------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "KG".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "KG".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-student-k"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("KG".lower() not in str(description).lower() or "Eastview".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-student-k"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-student-k------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "KG".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "KG".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-student-k"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("KG".lower() not in str(description).lower() or "Mifflin".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-student-k"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-student-k------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "KG".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "KG".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-student-k"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("KG".lower() not in str(description).lower() or "South".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-student-k"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-student-k,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-student-1------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "01".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "01".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-student-1"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("01".lower() not in str(description).lower() or "Eastview".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-student-1"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-student-1------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "01".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "01".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-student-1"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("01".lower() not in str(description).lower() or "Mifflin".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-student-1"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-student-1------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "01".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "01".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-student-1"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("01".lower() not in str(description).lower() or "South".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-student-1"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-student-1,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-student-2------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "02".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "02".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-student-2"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("02".lower() not in str(description).lower() or "Eastview".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-student-2"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-student-2------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "02".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "02".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-student-2"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("02".lower() not in str(description).lower() or "Mifflin".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-student-2"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-student-2------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "02".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "02".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-student-2"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("02".lower() not in str(description).lower() or "South".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-student-2"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-student-2,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-student-3------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "03".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "03".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-student-3"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("03".lower() not in str(description).lower() or "Eastview".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-student-3"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-student-3------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "03".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "03".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-student-3"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("03".lower() not in str(description).lower() or "Mifflin".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-student-3"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-student-3------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "03".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "03".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-student-3"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("03".lower() not in str(description).lower() or "South".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-student-3"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-student-3,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-student-4------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "04".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "04".lower() in str(description).lower() and "Eastview".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-student-4"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("04".lower() not in str(description).lower() or "Eastview".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-student-4"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-student-4------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "04".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "04".lower() in str(description).lower() and "Mifflin".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-student-4"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("04".lower() not in str(description).lower() or "Mifflin".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-student-4"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-student-4------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "04".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "04".lower() in str(description).lower() and "South".lower() \
        in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-student-4"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("04".lower() not in str(description).lower() or "South".lower() \
        not in str(location).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-student-4"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-student-4,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madhs-mail-student------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "High".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "High".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madhs-mail-student"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("High".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madhs-mail-student"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madhs-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madms-mail-student------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Middle".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Middle".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madms-mail-student"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Middle".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madms-mail-student"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madms-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madea-mail-student------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Eastview".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Eastview".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madea-mail-student"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Eastview".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madea-mail-student"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madea-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madmi-mail-student------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Mifflin".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Mifflin".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madmi-mail-student"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Mifflin".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madmi-mail-student"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madmi-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------madso-mail-student------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        description = i['attributes']['description']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        title = i['attributes']['title']
        if "CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "South".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "South".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to madso-mail-student"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("South".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from madso-mail-student"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=madso-mail-student,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )

    c.unbind()


cred()
main()
