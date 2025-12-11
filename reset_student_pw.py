#!/bin/env python3
'''Script to reset student passwords to their default value'''

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
import time

from ldap3 import ALL, Connection, Server, Tls


class Color:
    '''colors'''
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
    print(Color.DARKCYAN + "\n")
    print("*********************************")
    print("*      Python 3 Script For      *")
    print("*       Resetting Student       *")
    print("*  Active Directory Passwords   *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print("\n" + Color.END)


# Global Variables
with open("/home/lstrohm/Scripts/ADcreds.txt", mode="r", encoding="utf-8") as f:
    lines = f.readlines()
    user = lines[0]
    password = lines[1]
tls = Tls(
        local_private_key_file=None,
        local_certificate_file=None,
    )
server = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
conn = Connection(server, user=user.strip(),
               password=password.strip())


def reset_all(c):
    '''Resets all student passwords'''
    c.bind()
    c.search(
        "ou=Madison,dc=mlsd,dc=local",
        "(&(objectclass=person)(employeeID=*)",
        attributes=["displayName", "employeeID"],
    )
    users = c.entries
    print(
        Color.RED
        + "You are about to reset the password for ALL ACTIVE "
        + "STUDENTS!!!"
        + Color.END
    )
    sel = input(Color.YELLOW + "Are you sure? [y/N] " + Color.END)
    # If yes, the function continues. If no, the function returns to the menu
    # If yes or no not is given, the script errors out and exits
    if (
        sel == "y"
        or sel == "Y"
        or sel == "yes"
        or sel == "Yes"
        or sel == " YES"
    ):
        for i in users:
            dn = str(i.entry_dn)
            name = str(i.displayName.value)
            pw = str(i.employeeID)
            while len(pw) < 8:
                pw = "0" + pw
            print(
                "Resetting password for "
                + Color.CYAN
                + name
                + ": "
                + pw
                + Color.END
                + "."
            )
            c.extend.microsoft.modify_password(dn, pw)
        c.unbind()
        print(Color.GREEN + "Done!" + Color.END)
        time.sleep(1)
        exit()
    elif (
        sel == "n"
        or sel == "N"
        or sel == "no"
        or sel == "No"
        or sel == "NO"
        or sel == ""
    ):
        c.unbind()
        time.sleep(1)
        exit()
    else:
        print(Color.RED + "Error!" + Color.END)
        time.sleep(1)
        c.unbind()
        exit()


def reset_single(c, username):
    '''Resets single student's password'''
    c.bind()
    try:
        c.search(
            "ou=Madison,dc=mlsd,dc=local",
            "(&(objectclass=person)(employeeID=*)(cn=*"
            + username + "*))",
            attributes=["employeeID", "displayName"],
        )
        users = c.entries
        if len(users) <= 0:
            raise IndexError
        print(Color.BOLD + "\nI found the following students:\n" + Color.END)
        ent = 0
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
                + ", Student ID: "
                + Color.GREEN
                + str(users[ent].employeeID)
                + Color.END
            )
            ent = ent + 1
        usn = int(
            input(
                Color.BOLD
                + "\nPlease select a student you wish"
                + " to reset the password for: "
                + Color.END
            )
        )
        student_user = c.entries[usn]
        name = str(student_user.displayName.value)
        dn = str(student_user.entry_dn)
        pw = str(student_user.employeeID)
        while len(pw) < 8:
            pw = "0" + pw
        print(
            Color.BOLD
            + "You are about to reset the password for "
            + Color.YELLOW
            + name
            + Color.END
            + " to "
            + Color.YELLOW
            + pw
            + Color.END
            + "."
        )
        sel = input(Color.BOLD + "Is this correct? [Y/n] " + Color.END)
        # If yes, the function continues. If no, the function restarts
        # If yes or no is not given, the script errors out and exits
        if (
            sel == "y"
            or sel == "Y"
            or sel == "yes"
            or sel == ""
            or sel == "Yes"
            or sel == "YES"
        ):
            print(
                "\nResetting Password for "
                + Color.CYAN
                + name
                + Color.END
                + " to "
                + Color.CYAN
                + pw
                + Color.END
                + "."
            )
            c.extend.microsoft.modify_password(dn, pw)
            c.unbind()
            print(Color.GREEN + "Done!" + Color.END)
            time.sleep(1)
            exit()
        elif (
            sel == "n"
            or sel == "N"
            or sel == "no"
            or sel == "No"
            or sel == "NO"
        ):
            c.unbind()
            time.sleep(1)
            exit()
        else:
            print(Color.RED + "Error!" + Color.END)
            time.sleep(1)
            c.unbind()
            exit()
    except IndexError:
        print(
            Color.RED
            + "Username not found or not a student! Try "
            + "again.\n"
            + Color.END
        )
    except KeyboardInterrupt:
        print(
            Color.BOLD
            + Color.CYAN
            + "\nCtrl-C detected. Exiting...\n"
            + Color.END
        )



if __name__ == "__main__":
    # Sets up parser and adds arguement
    parser = argparse.ArgumentParser(
        description="Script to reset a student\
                                    password to its default value"
    )
    parser.add_argument(
        "user_name",
        metavar="Username",
        default="",
        type=str,
        help="Username or last name of student",
        nargs="?",
    )
    parser.add_argument(
        "-a",
        "--all",
        metavar="All",
        default=False,
        action="store_const",
        const=True,
        help="Reset all \
                        students' passwords",
    )
    args = parser.parse_args()
    user_name = args.user_name
    all_stu = args.all

    cred()

    if all_stu is True and user_name == "":
        reset_all(conn)
    elif all_stu is False and len(user_name) > 0:
        reset_single(conn, user_name)
    elif user_name == "" and all_stu is False:
        parser.print_help()
        parser.exit(1)
