#!/usr/bin/env python3


import csv
from ldap3 import ALL, Connection, Server, Tls

# Connects  and binds to LDAP server
with open("/home/lstrohm/Scripts/ADcreds.txt", mode="r", encoding="utf-8") as f:
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


def main(con):
    """Main function"""
    with open(
        "/home/lstrohm/Website_Directory_Combined.csv", mode="w", encoding="utf-8"
    ) as wdc:
        writer = csv.writer(wdc)
        headers = [
            "Primary Department",
            "Title",
            "First Name",
            "Last Name",
            "Email",
            "Phone Number",
            "Building",
        ]
        writer.writerow(headers)
        r = open("/home/lstrohm/Website_Directory.csv", mode="r", encoding="utf-8")
        reader = csv.reader(r)
        next(reader)
        for title, fn, ln, bldg in reader:
            title = str(title).strip()
            fn = str(fn).strip()
            ln = str(ln).strip()
            bldg = str(bldg).strip()

            con.search(
                "ou=Madison,dc=mlsd,dc=local",
                "(&(objectclass=person)(givenName=*" + fn + "*)(sn=*" + ln + "*))",
                attributes=["mail", "givenName", "sn", "telephoneNumber"],
            )
            user = con.entries

            if len(str(user)) <= 5:
                data = ["", title, fn, ln, "", "", bldg]
            else:
                data = [
                    "",
                    title,
                    fn,
                    ln,
                    str(user[0].mail.value).strip().lower(),
                    str(user[0].telephoneNumber.value).strip(),
                    bldg,
                ]

            writer.writerow(data)
        r.close()
    wdc.close()


if __name__ == "__main__":
    main(c)
