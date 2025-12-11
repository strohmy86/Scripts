#!/usr/bin/env python3
'''Scripts to disable a user's account in AD'''

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


from argparse import ArgumentParser
import datetime
import os
import time

import paramiko
from ldap3 import ALL, MODIFY_DELETE, MODIFY_REPLACE, Connection, Server, Tls


class Color:
    """Class for text colors"""
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
    """Simply print credits of the script"""
    print(
        Color.DARKCYAN
        + "\n"
        + "**********************************\n"
        + "* Python 3 Script For Disabling  *\n"
        + "* Accounts in Active Directory   *\n"
        + "* Moving Them to the Disabled OU *\n"
        + "*                                *\n"
        + "*   Written and maintained by    *\n"
        + "*          Luke Strohm           *\n"
        + "*     strohm.luke@gmail.com      *\n"
        + "*  https://github.com/strohmy86  *\n"
        + "**********************************\n"
        + "\n"
        + Color.END
    )


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
con = Connection(s, user=username.strip(), password=password.strip())
con.bind()
# Global Variables
dis_ou = ",ou=Disabled,ou=Madison,dc=mlsd,dc=local"
today = str(datetime.datetime.now())
today2 = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S.%f")
right_now = today2.strftime("%m-%d-%Y at %H:%M")
# Specify private key file
k = paramiko.RSAKey.from_private_key_file("/home/lstrohm/.ssh/id_rsa")
# Connects to gcds server via SSH
gcds_server = paramiko.SSHClient()
gcds_server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
gcds_server.connect("madhs01gcds.mlsd.local", username="mlsd\\administrator", pkey=k)


def single(c, usr, disabled_ou, now):
    """Searches AD and return results to choose for account disable."""
    try:
        c.search(
            "ou=Madison,dc=mlsd,dc=local",
            "(&(objectclass=person)(cn=*" + usr + "*))",
            attributes=[
                "mail",
                "title",
                "displayName",
                "lastLogon",
                "userAccountControl",
                "cn",
                "description",
                "memberOf",
                "physicalDeliveryOfficeName",
                "company",
            ],
        )
        users = c.entries
        if len(users) <= 0:
            raise IndexError
        ent = 0  # Start of result list
        print(Color.BOLD + Color.CYAN + "I found the following user(s):\n" + Color.END)
        for i in users:
            if "514" in str(users[ent].userAccountControl.value) or "546" in str(
                users[ent].userAccountControl.value
            ):
                status = "Disabled"
            elif "512" in str(users[ent].userAccountControl.value) or "544" in str(
                users[ent].userAccountControl.value
            ):
                status = "Active"
            else:
                status = "Unknown"
            print(
                str(ent)
                + ")  Name: "
                + Color.GREEN
                + str(users[ent].displayName.value)
                + Color.END
                + ", AD Location: "
                + Color.GREEN
                + str(users[ent].entry_dn)
                + Color.END
                + ", Title: "
                + Color.GREEN
                + str(users[ent].title.value)
                + Color.END
                + ", Status: "
                + Color.GREEN
                + status
                + Color.END
            )
            ent = ent + 1  # Moves to next in results list
        # Prompts to select user from search results
        usn = int(input(Color.BOLD + "\nPlease select a user: " + Color.END))
        user = c.entries[usn]
        print(
            Color.YELLOW
            + "Disabling account "
            + Color.BOLD
            + user.cn.value
            + Color.END
            + Color.YELLOW
            + " and moving it "
            + "to the disabled OU."
            + Color.END
        )
        if isinstance(user.memberOf.value, list) is True:
            c.modify(
                str(user.entry_dn),
                {
                    "description": [(MODIFY_DELETE, [])],
                },
            )
            c.modify(
                str(user.entry_dn),
                {
                    "memberOf": [(MODIFY_DELETE, [])],
                },
            )
            time.sleep(0.500)
            for i in user.memberOf.value:
                c.modify(
                    str(i),
                    {
                        "member": [(MODIFY_DELETE, [str(user.entry_dn)])],
                    },
                )
                time.sleep(0.300)
        elif isinstance(user.memberOf.value, str) is True:
            c.modify(
                str(user.entry_dn),
                {
                    "description": [(MODIFY_DELETE, [])],
                },
            )
            c.modify(
                str(user.entry_dn),
                {
                    "memberOf": [(MODIFY_DELETE, [])],
                },
            )
            time.sleep(0.500)
            c.modify(
                user.memberOf.value,
                {"member": [(MODIFY_DELETE, [str(user.entry_dn)])]},
            )
            time.sleep(0.500)
        c.modify(
            str(user.entry_dn),
            {
                "userAccountControl": [(MODIFY_REPLACE, ["514"])],
            },
        )
        c.modify(
            str(user.entry_dn),
            {
                "description": [(MODIFY_REPLACE, ["Disabled - " + str(now)])],
            },
        )
        time.sleep(0.500)
        if "student" in str(user.company.value) and "Adult" in str(
            user.physicalDeliveryOfficeName.value
        ):
            disabled_ou = (
                "ou=AdultEd,ou=Disabled,ou=Student,ou=Madison,dc=mlsd,dc=local"
            )
        elif "staff" in str(user.company.value):
            disabled_ou = "ou=Staff" + disabled_ou
        else:
            disabled_ou = (
                "ou="
                + str(datetime.date.today().year)
                + ",ou=Disabled,"
                + "ou=Student,ou=Madison,dc=mlsd,dc=local"
            )

        c.modify_dn(
            str(user.entry_dn),
            "cn=" + str(user.cn.value),
            new_superior=disabled_ou,
        )
        cmd = "/home/lstrohm/bin/gamadv-xtd3/gam user " + str(user.cn.value) + " deprov"
        os.system(cmd)
        cmd2 = "/home/lstrohm/bin/gamadv-xtd3/gam create transfer "\
            + str(user.cn.value) + " drive vault"
        os.system(cmd2)

    except IndexError:  # Error received if empty search result
        print(Color.RED + "No username found! Try again.\n" + Color.END)
    except KeyboardInterrupt:  # User exited script with CTRL + C
        print(Color.CYAN + "\nExiting..." + Color.END)
        exit()


def batch(c, file, disabled_ou, now):
    """Runs script in batch mode using a file with CNs"""
    try:
        with open(file, mode="r", encoding="utf-8") as f:
            for i in f:
                i = str(i).strip()
                # i = i[2:-2]
                c.search(
                    "ou=Madison,dc=mlsd,dc=local",
                    "(CN=" + i + ")",
                    attributes=[
                        "mail",
                        "title",
                        "displayName",
                        "lastLogon",
                        "userAccountControl",
                        "cn",
                        "description",
                        "memberOf",
                        "physicalDeliveryOfficeName",
                        "company",
                    ],
                )
                user = c.entries
                if len(user) <= 0:
                    raise IndexError
                user = user[0]
                print(
                    Color.YELLOW
                    + "Disabling account "
                    + Color.BOLD
                    + user.cn.value
                    + Color.END
                    + Color.YELLOW
                    + " and moving it "
                    + "to the disabled OU."
                    + Color.END
                )
                if isinstance(user.memberOf.value, list) is True:
                    c.modify(
                        str(user.entry_dn),
                        {
                            "description": [(MODIFY_DELETE, [])],
                        },
                    )
                    c.modify(
                        str(user.entry_dn),
                        {
                            "memberOf": [(MODIFY_DELETE, [])],
                        },
                    )
                    time.sleep(0.500)
                    for i in user.memberOf.value:
                        c.modify(
                            str(i),
                            {
                                "member": [(MODIFY_DELETE, [str(user.entry_dn)])],
                            },
                        )
                        time.sleep(0.300)
                elif isinstance(user.memberOf.value, str) is True:
                    c.modify(
                        str(user.entry_dn),
                        {
                            "description": [(MODIFY_DELETE, [])],
                        },
                    )
                    c.modify(
                        str(user.entry_dn),
                        {
                            "memberOf": [(MODIFY_DELETE, [])],
                        },
                    )
                    time.sleep(0.500)
                    c.modify(
                        user.memberOf.value,
                        {"member": [(MODIFY_DELETE, [str(user.entry_dn)])]},
                    )
                    time.sleep(0.500)
                c.modify(
                    str(user.entry_dn),
                    {
                        "userAccountControl": [(MODIFY_REPLACE, ["514"])],
                    },
                )
                c.modify(
                    str(user.entry_dn),
                    {
                        "description": [(MODIFY_REPLACE, ["Disabled - " + str(now)])],
                    },
                )
                time.sleep(0.500)
                if "student" in str(user.company.value) and "Adult" in str(
                    user.physicalDeliveryOfficeName.value
                ):
                    disabled_ou = (
                        "ou=AdultEd,ou=Disabled,ou=Student,ou=Madison,dc=mlsd,dc=local"
                    )
                elif "staff" in str(user.company.value):
                    disabled_ou = "ou=Staff" + disabled_ou
                else:
                    disabled_ou = (
                        "ou="
                        + str(datetime.date.today().year)
                        + ",ou=Disabled,"
                        + "ou=Student,ou=Madison,dc=mlsd,dc=local"
                    )

                c.modify_dn(
                    str(user.entry_dn),
                    "cn=" + str(user.cn.value),
                    new_superior=disabled_ou,
                )
                print(c.result)
                time.sleep(0.500)
                cmd = (
                    "/home/lstrohm/bin/gamadv-xtd3/gam user "
                    + str(user.cn.value)
                    + " deprov"
                )
                os.system(cmd)
                cmd2 = (
                    "/home/lstrohm/bin/gamadv-xtd3/gam create transfer "
                    + str(user.cn.value)
                    + " drive vault"
                )
                os.system(cmd2)
        f.close()
    except IndexError:  # Error received if empty search result
        print(
            Color.RED
            + "Error in file! User not found. Check your file"
            + "and try again.\n"
            + Color.END
        )

def run_gcds(gcds):
    '''Runs gcds after account(s) is/are disabled'''
    print(Color.CYAN + Color.BOLD + "Running GCDS. Please wait....." + Color.END)
    # Connects to madhs01gcds server via SSH and runs a Google Sync
    stdin, stdout, stderr = gcds.exec_command("C:\\Tools\\gcds.cmd")
    for line in stdout:
        print(Color.YELLOW + line.strip("\n") + Color.END)
    print(Color.GREEN + "\nDone!\n" + Color.END)
    gcds.close()

# Sets up parser and adds arguements
def main():
    '''Main function'''
    parser = ArgumentParser(description="Script to disable user accounts.")
    parser.add_argument(
        "usr",
        metavar="Username",
        default="",
        type=str,
        help="Username or last name of user to disable.",
        nargs="?",
    )
    parser.add_argument(
        "-b",
        "--batch",
        metavar="Filename",
        default="",
        type=str,
        help="Batch mode with a text file (one username per line).",
    )
    args = parser.parse_args()
    usr = args.usr
    file = args.batch

    cred()

    if file == "" and usr != "":
        single(con, usr, dis_ou, right_now)
        con.unbind()
        run_gcds(gcds_server)
    elif file != "" and usr == "":
        batch(con, file, dis_ou, right_now)
        con.unbind()
        run_gcds(gcds_server)
    else:
        con.unbind()
        gcds_server.close()
        parser.print_help()
        parser.exit(1)

    


if __name__ == "__main__":
    main()
