#!/usr/bin/env python3

import csv
from ldap3 import ALL, MODIFY_REPLACE, Connection, Server, Tls


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


with open("/home/lstrohm/Staff_Needed_Phone_Numbers.csv", "r", encoding="utf-8") as fa:
    reader = csv.reader(fa)
    next(reader)  # Skip header row
    for l_name, f_name, phone, email, bldg, title in reader:
        l_name = str(l_name).strip()
        f_name = str(f_name).strip()
        phone = str(phone).strip()
        email = str(email).strip()
        bldg = str(bldg).strip()
        title = str(title).strip()

        c.search(
            "ou=Madison,dc=mlsd,dc=local",
            "(&(objectclass=person)(mail=*" + email + "*))",
            attributes=[
                "mail",
                "givenName",
                "sn",
                "mobile",
                "title",
                "physicalDeliveryOfficeName",
                "department",
            ],
        )
        user = c.entries
        if len(user) == 0:
            continue
        if user[0].mobile.value is not None:
            continue
        c.modify(
            str(user[0].entry_dn),
            {
                "mobile": [(MODIFY_REPLACE, [phone])],
            },
        )

    fa.close()
c.unbind()
