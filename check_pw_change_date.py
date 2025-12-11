#!/usr/bin/env python3
'''Script to see when a user last changed their AD password'''

# MIT License

# Copyright (c) 2020 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import datetime

from ldap3 import ALL, Connection, Server, Tls


class Color:
    '''Colors'''
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
    '''Credentials'''
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "*    Utility to Check When      *\n"
        + "*    A Password Was Changed     *\n"
        + "*                               *\n"
        + "*  Written and maintained by:   *\n"
        + "*         Luke Strohm           *\n"
        + "*     strohm.luke@gmail.com     *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def main(username):
    '''Main function'''
    # Connect and bind to LDAP server
    with open("/home/lstrohm/Scripts/ADcreds.txt", mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        usern = lines[0].strip()
        password = lines[1].strip()
    tls = Tls(
            local_private_key_file=None,
            local_certificate_file=None,
        )
    s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
    c = Connection(s, user=usern, password=password)
    c.bind()
    # Search for user. Lists all usernames matching string provided.
    try:
        c.search(
            "ou=Madison,dc=mlsd,dc=local",
            f"(&(objectclass=person)(|(cn=*{username}*)(displayName=*{username}*)))",
            attributes=[
                "title",
                "displayName",
                "pwdLastSet",
            ],
        )
        users = c.entries
        if len(users) <= 0:
            raise IndexError
        print(Color.BOLD + "\nI found the following users:\n" + Color.END)
        ent = 0  # Start of result list
        for i in users:
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
                + str(users[ent].title)
                + Color.END
            )
            ent = ent + 1  # Moves to next in results list
        # Prompts to select user from search results
        usn = int(input(Color.BOLD + "\nPlease select a user: " + Color.END))
        user = c.entries[usn]
        name = str(user.displayName.value)
        setstr = str(user.pwdLastSet.value)[:-22]
        setdate = datetime.datetime.strptime(setstr, "%Y-%m-%d")
        set_str = setdate.strftime("%m-%d-%Y")  # Pretty date
        print(
            Color.GREEN
            + name
            + Color.END
            + " changed their password on "
            + Color.YELLOW
            + set_str
            + Color.END
        )
        c.unbind()
    except IndexError:  # Error received if empty search result
        print(Color.RED + "No username found! Try again.\n" + Color.END)
    except KeyboardInterrupt:  # User exited script with CTRL + C
        print(Color.CYAN + "\nCtrl-C detected. Exiting..." + Color.END)
        exit()


if __name__ == "__main__":
    # Sets up parser and adds arguement
    parser = argparse.ArgumentParser(
        description="Script to check the password\
                                    expiration date for a user."
    )
    parser.add_argument(
        "user_name",
        metavar="Username",
        default="",
        type=str,
        help="Username of user to check.",
    )
    args = parser.parse_args()

    cred()
    main(args.user_name)
