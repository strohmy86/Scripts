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
        search_filter="(&(mail=*)(objectClass=person)(!(cn=*Sub*)))",
        search_scope=SUBTREE, attributes=["cn", 
                                          "memberOf", 
                                          "physicalDeliveryOfficeName", 
                                          "userAccountControl",
                                          "department"
                                          ],
        paged_size=5, generator=False
    )

    
    #------------------------------all-so------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "South".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "South".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-so"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("South".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-so"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-so,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )
            

    #------------------------------all-mi------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Mifflin".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Mifflin".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-mi"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Mifflin".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-mi"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-mi,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )
            

    #------------------------------all-ea------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Eastview".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Eastview".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-ea"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Eastview".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-ea"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-ea,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------all-hs------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "High".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "High".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-hs"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("High".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-hs"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-hs,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    #------------------------------all-ms------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Middle".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Middle".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-ms"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Middle".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-ms"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-ms,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )        
            

    #------------------------------all-lh------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        if "CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and "Early Childhood".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and "Early Childhood".lower() in str(location).lower() and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-lh"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Early Childhood".lower() not in str(location).lower() or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-lh"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-lh,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )
            

    #------------------------------all-ae------------------------------#
    for i in users:
        dn = i['dn']
        cn = i['attributes']['cn']
        memberOf = i['attributes']['memberOf']
        location = i['attributes']['physicalDeliveryOfficeName']
        status = i['attributes']['userAccountControl']
        department = i['attributes']['department']
        if "CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and ("Adult".lower() in str(location).lower() or "Adult".lower() in \
        str(department).lower()) and "514" not in str(status) and "546" not in str(status):
            continue
        elif "CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(memberOf) \
        and ("Adult".lower() in str(location).lower() or "Adult".lower() in \
        str(department).lower()) and "514" not in str(status) and "546" not in str(status):
            print(
            Color.CYAN
            + "Adding "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.CYAN
            + " to all-ae"
            + Color.END
            )   
            c.modify(
            str(dn),
            {
                "memberOf": [
                    (MODIFY_ADD, ["CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                ],
            },
            )
            time.sleep(0.5)
            c.modify(
                "CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                {
                   "member": [(MODIFY_ADD, [str(dn)])],
                },
            )
        elif "CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(memberOf) \
        and (("Adult".lower() not in str(location).lower() or "Adult".lower() \
        not in str(department).lower()) or "514" in str(status) or "546" in str(status)):
            print(
            Color.YELLOW
            + "Removing "
            + Color.BOLD
            + str(cn)
            + Color.END
            + Color.YELLOW
            + " from all-ae"
            + Color.END
            )
            c.modify(
                str(dn),
                {
                    "memberOf": [
                        (MODIFY_DELETE, ["CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local"])
                    ],
                },
            )
            time.sleep(0.5)
            c.modify(
                    "CN=all-ae,OU=Groups,OU=Madison,DC=mlsd,DC=local",
                    {"member": [(MODIFY_DELETE, [str(dn)])]},
                )


    c.unbind()

main()