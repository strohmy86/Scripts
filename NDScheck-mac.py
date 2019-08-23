#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This script will run NDSrepair on a selected server and report any errors

import sys
import time
import paramiko

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

print(Color.DARKCYAN + '\n')
print("*********************************")
print("*      NDScheck Utility         *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n" + Color.END)


def main(server):

    # Specify private key file
    k = paramiko.RSAKey.from_private_key_file('/Users/lstrohm/.ssh/Identityrsa')

    # Configure SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username='root', pkey=k)

    # Checks NDS time sync
    print(Color.YELLOW+'Checking NDS time sync...'+Color.END)
    stdin, stdout, stderr = client.exec_command('ndsrepair -T')
    for line in stdout:
        print(line.strip('\n'))
    print('\n')

    # Prompts user to run more tests
    e = input(Color.CYAN+'Would you like to continue checks? [Y/n]:  '+Color.END)
    if e == 'y' or e == 'yes' or e == '':
        print(Color.YELLOW+'Checking NDS replication status...'+Color.END)
        stdin, stdout, stderr = client.exec_command('ndsrepair -E')
        for line in stdout:
            print(line.strip('\n'))
        print('\n')
    elif e != 'y' or e != 'yes' or e != '':
        print(COlor.GREEN+'Exiting.'+Color.END)
        client.close()
        menu()

    # Prompts user to run the last test
    n = input(Color.CYAN+'Would you like to run the last check? [Y/n]:  '+Color.END)
    if n == 'y' or n == 'yes' or n == '':
        print(Color.YELLOW+'Checking NDS server status...'+Color.END)
        stdin, stdout, stderr = client.exec_command('ndsrepair -N')
        time.sleep(1)
        stdin.write('\n')
        time.sleep(1)
        stdin.write('q\n')
        stdin.flush()
        data = stdout.read().splitlines()
        for line in data:
            print(line)
        print('\n')
        input(Color.GREEN+'Press Enter to continue...'+Color.END)
    elif n != 'y' or n != 'yes' or n != '':
        print(Color.GREEN+'Exiting.'+Color.END)
        client.close()
        menu()


def menu():

    # Generate the menu.
    while True:
        print('\n')
        print(Color.PURPLE + 'Menu:' + Color.END)
        print('\n')
        print('1)  MADHS01STAFF1')
        print('2)  MADHS01STU1')
        print('3)  MADHS01WEB1')
        print('4)  MADHS01IDM')
        print('5)  MADHS01GW1')
        print('6)  MADMS01FP1')
        print('7)  MADEA01FP1')
        print('8)  MADMI01FP1')
        print('9)  MADSO01FP1')
        print('0)  Exit')
        print('\n')

        # Prompts user to select a menu item.
        selection = input(Color.BOLD+'Please Choose a Server: '+Color.END)

        # Sets the server variable based on menu selection then executes the main function.
        if selection == '1':
            server = 'madhs01staff1.mlsd.net'
            main(server)
        elif selection == '2':
            server = 'madhs01stu1.mlsd.net'
            main(server)
        elif selection == '3':
            server = 'madhs01web1.mlsd.net'
            main(server)
        elif selection == '4':
            server = 'madhs01idm.mlsd.net'
            main(server)
        elif selection == '5':
            server = 'madhs01gw1.mlsd.net'
            main(server)
        elif selection == '6':
            server = 'madms01fp1.mlsd.net'
            main(server)
        elif selection == '7':
            server = 'madea01fp1.mlsd.net'
            main(server)
        elif selection == '8':
            server = 'madmi01fp1.mlsd.net'
            main(server)
        elif selection == '9':
            server = 'madso01fp1.mlsd.net'
            main(server)
        elif selection == '0':
            sys.exit()
        else:
            print(Color.RED+'Unknown Option Selected!'+Color.END)
            time.sleep(2)
            menu()

# Starts the script.


menu()
