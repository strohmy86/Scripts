#!/usr/bin/env python3

'''MIT License
Copyright (c) 2020 Luke Strohm
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


import argparse
import os
import shutil

from ldap3 import ALL, Connection, Server, Tls


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
        + "*     Photo Renaming Script     *\n"
        + "*                               *\n"
        + "*  Written and maintained by:   *\n"
        + "*        Luke Strohm            *\n"
        + "*    strohm.luke@gmail.com      *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*                               *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def main(source):
    '''Main Function'''
    # Connect and bind to LDAP server.
    f = open("/home/lstrohm/Scripts/ADcreds.txt", mode="r", encoding="UTF-8")
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
    dst = "/home/lstrohm/Photos/Students/"
    for filename in os.listdir(source):
        ids = filename.replace(".jpg", "")
        c.search(
            "ou=Student,ou=Madison,dc=mlsd,dc=local",
            "(&(objectclass=Person)(title=" + ids + "))",
            attributes=["title", "mail", "cn"],
        )
        results = c.entries
        # If student not found in LDAP, skips them
        if len(results) <= 0:
            pass
        else:
            nimg = str(results[0].cn.value) + ".jpg"
            dest = dst + nimg.lower()
            src = source + filename
            shutil.copy(src, dest)
    c.unbind()


# Creates parser and adds arguements
parser = argparse.ArgumentParser(
    description="Script to rename student school photos"
)
parser.add_argument(
    "source",
    metavar="Source",
    default="",
    type=str,
    help="Source image directory.",
)
args = parser.parse_args()
source = args.source

cred()
main(source)
