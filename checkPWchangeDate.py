#!/usr/bin/env python3

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
import time

from ldap3 import ALL, Connection, Server


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def cred():
    print(Color.DARKCYAN + '\n' +
          '*********************************\n' +
          '*    Utility to Check When      *\n' +
          '*    A Password Was Changed     *\n' +
          '*                               *\n' +
          '*  Written and maintained by:   *\n' +
          '*        Luke Strohm            *\n' +
          '*    strohm.luke@gmail.com      *\n' +
          '*  https://github.com/strohmy86 *\n' +
          '*********************************\n' +
          '\n' + Color.END)


def main(username):
    today = str(datetime.datetime.today())[:-16]
    today2 = datetime.datetime.strptime(today, '%Y-%m-%d')
    # Connect and bind to LDAP server
    s = Server('madhs01staff1.mlsd.net', use_ssl=True, get_info=ALL)
    c = Connection(s)
    c.bind()
    # Search for user. Lists all usernames matching string provided.
    try:
        c.search('o=Madison', '(&(objectclass=inetOrgPerson)' +
                 '(cn=*'+username+'*))',
                 attributes=['title', 'fullName', 'passwordExpirationTime',
                             'loginGraceRemaining'])
        users = c.entries
        if len(users) <= 0:
            raise IndexError
        print(Color.BOLD + '\nI found the following users:\n' +
              Color.END)
        ent = 0  # Start of result list
        for i in users:
            print(str(ent)+')  Name: '+Color.GREEN+str(users[ent].
                  fullName.value)+Color.END+', eDir Location: ' +
                  Color.GREEN+str(users[ent].entry_dn)+Color.END +
                  ', Title: '+Color.GREEN+str(users[ent].title) +
                  Color.END)
            ent = ent + 1  # Moves to next in results list
        # Prompts to select user from search results
        usn = int(input(Color.BOLD+'\nPlease select a user: ' + Color.END))
        user = c.entries[usn]
        name = str(user.fullName.value)
        grace = str(user.loginGraceRemaining.value)
        expstr = str(user.passwordExpirationTime.value)[:-15]
        expdate = datetime.datetime.strptime(expstr, '%Y-%m-%d')
        chgDate = expdate - datetime.timedelta(days=90)  # Checks PW change
        dateStr = chgDate.strftime('%m-%d-%Y')  # Pretty date
        expStr = expdate.strftime('%m-%d-%Y')  # Pretty date
        if today2 > expdate:  # If PW is expired
            print(Color.RED+name+'\'s password expired on '+expStr+'!' +
                  Color.END)
            print(Color.YELLOW+'They have '+grace+' grace logins remaining' +
                  Color.END)
        else:  # PW not expired
            print(Color.GREEN+name+'\'s' + Color.END+' password expires on ' +
                  Color.CYAN+expStr+Color.END)
            print(Color.GREEN+name+Color.END+' changed their password on ' +
                  Color.YELLOW + dateStr + Color.END)
        time.sleep(1)
        c.unbind()
    except IndexError:  # Error received if empty search result
        print(Color.RED + 'No username found! Try again.\n' + Color.END)
    except KeyboardInterrupt:  # User exited script with CTRL + C
        print(Color.CYAN+'\nExiting...'+Color.END)
        exit()


# Sets up parser and adds arguement
parser = argparse.ArgumentParser(description='Script to check the password\
                                 expiration date for a user.')
parser.add_argument('username', metavar='Username', default='', type=str,
                    help='Username of user to check.')
args = parser.parse_args()
username = args.username


cred()
main(username)
