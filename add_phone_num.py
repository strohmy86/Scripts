#!/usr/bin/env python3
'''Script to add cell phone numbers to users in AD'''

# MIT License

# Copyright (c) 2025 Luke Strohm

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

import csv
from argparse import ArgumentParser
import phonenumbers

from ldap3 import (
    ALL,
    MODIFY_REPLACE,
    Connection,
    Server,
    Tls,
)

def format_phone_number(phone_number, region="US"):
    '''formats the cell number to standard format (###) ###-####'''
    try:
        # Parse the number, specifying a default region if no country code is present
        pn = phonenumbers.parse(phone_number, region)
        # Format the number into the national format (which uses parentheses for US numbers)
        return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL)
    except phonenumbers.NumberParseException:
        return "Invalid phone number"


def main(user_list):
    '''Main Function'''
    # Connects  and binds to LDAP server
    with open("/home/lstrohm/Scripts/ADcreds.txt", "r", encoding="utf-8") as creds:
        lines = creds.readlines()
        username = lines[0]
        password = lines[1]
    tls = Tls(
        local_private_key_file=None,
        local_certificate_file=None,
    )
    s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
    c = Connection(s, user=username.strip(), password=password.strip())
    c.bind()
    with open(user_list, mode="r", encoding="utf-8") as fa:
        reader = csv.reader(fa)
        for cell, cn in reader:
            try:
                cell = str(format_phone_number(cell))
                cn = str(cn).strip()
                c.search(
                    "o=Madison",
                    "(&(objectclass=Person)(cn=" + cn + "))",
                    attributes=["mobile", "fullName"],
                )
                user = c.entries[0]
                dn = str(user.entry_dn)
                c.modify(dn, {"mobile": [(MODIFY_REPLACE, [cell])]})
            except IndexError:
                continue
    fa.close()
    c.unbind()


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Script to add cellphone numbers."
    )
    parser.add_argument(
        "file",
        metavar="File",
        default="",
        type=str,
        help="Name of CSV File.",
    )

    args = parser.parse_args()
    lst = args.file

    if len(lst) > 0:
        main(lst)
    else:
        parser.print_help()
        parser.exit(1)
