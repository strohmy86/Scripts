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


import argparse
import csv
import os
import shutil

from ldap3 import ALL, Connection, Server


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


def main(filename, source):
    # Connect and bind to LDAP server.
    s = Server("madhs01staff1.mlsd.net", use_ssl=True, get_info=ALL)
    c = Connection(s)
    c.bind()
    filename2 = filename.split("/")[-1]
    # Open file2 for writing
    with open(
        "/home/lstrohm/" + filename2[:-4] + "-renamed.csv", mode="w"
    ) as fh:
        writer = csv.writer(fh)
        headers = [
            "Student ID",
            "Email",
            "New Image",
            "Old Image",
            "Grade",
            "Location",
        ]
        writer.writerow(headers)  # Write header row
        fs = open(filename, mode="r")  # Open source file for parsing
        reader = csv.reader(fs)
        next(reader)  # Skip header row
        # Searches LDAP for each student in source file, writes data to file 2
        for ids, img, first, grade, last, bldg in reader:
            c.search(
                "o=Madison",
                "(&(objectclass=inetOrgPerson)" + "(workforceID=" + ids + "))",
                attributes=["workforceID", "mail", "cn"],
            )
            results = c.entries
            # If student not found in LDAP, skips them
            if len(results) <= 0:
                pass
            else:
                user = results[0]
                data = [
                    ids,
                    user.mail.value,
                    user.cn.value + ".jpg",
                    img,
                    grade,
                    bldg,
                ]
                writer.writerow(data)
        fs.close()
    fh.close()
    c.unbind()
    # Re-opens file2 in read mode for parsing
    with open(
        "/home/lstrohm/" + filename2[:-4] + "-renamed.csv", mode="r"
    ) as fa:
        reader2 = csv.reader(fa)
        next(reader2)  # skip header row
        # Iterates through file2 and renames photo files.
        for ids, mail, nimg, oimg, gr, bldg in reader2:
            img = nimg.lower()
            dst = source + img
            src = source + oimg
            os.rename(src, dst)
    fa.close()
    files = os.listdir(source)
    dst = "/home/lstrohm/Pictures/Students/"
    for f in files:  # Moves photos to a single dir, overwriting existing.
        if os.path.exists(dst + f):
            os.remove(dst + f)
        shutil.move(source + f, dst)


# Creates parser and adds arguements
parser = argparse.ArgumentParser(
    description="Script to rename student\
                                 school photos"
)
parser.add_argument(
    "filename",
    metavar="Filename",
    default="",
    type=str,
    help="CSV file that contains student IDs and photo names",
)
parser.add_argument(
    "-s",
    "--source",
    metavar="source",
    default="",
    type=str,
    help="Source image directory.",
)
args = parser.parse_args()
filename = args.filename
source = args.source

cred()
main(filename, source)
