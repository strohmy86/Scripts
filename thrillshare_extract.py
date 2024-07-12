#!/usr/bin/env python3
"""Script to extract staff contact information from Active Directory for use
in the Thrillshare platform"""

# MIT License

# Copyright (c) 2024 Luke Strohm

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

from ldap3 import ALL, Connection, Server, Tls
import pandas as pd


# Connects  and binds to LDAP server
with open("/home/lstrohm/Scripts/ADcreds.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    username = lines[0]
    password = lines[1]

tls = Tls(
    local_private_key_file=None,
    local_certificate_file=None,
)
s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
c = Connection(s, user=username.strip(), password=password.strip())
c.bind()
# Searches Active Directory for active staff members that have a phone number.
c.search(
    "ou=Madison,dc=mlsd,dc=local",
    "(&(objectClass=person)(company=staff)(!(userAccountControl=514))\
    (!(userAccountControl=546))(mobile=*))",
    attributes=[
        "sn",
        "givenName",
        "mail",
        "mobile",
        "physicalDeliveryOfficeName",
        "department",
        "title",
    ],
)
users = c.entries  # Stores search results
# stores users in a pandas DataFrame
df = pd.DataFrame(
    [
        {
            "sn": x.sn.value,
            "givenName": x.givenName.value,
            "mail": x.mail.value,
            "mobile": x.mobile.value,
            "physicalDeliveryOfficeName": x.physicalDeliveryOfficeName.value,
            "department": x.department.value,
            "title": x.title.value,
        }
        for x in users
    ]
)
# Sorts the DataFrame by last name and formats the cell number.
df = df.sort_values(by=["sn"], ascending=True)
df["mobile"] = df["mobile"].str.replace("(", "")
df["mobile"] = df["mobile"].str.replace(")", "")
df["mobile"] = df["mobile"].str.replace("-", "")
# Converts the DataFrame to csv file for ingestion into Thrillshare.
df.to_csv("~/HomeDirectory/Staff.csv", encoding="utf-8", index=False)
