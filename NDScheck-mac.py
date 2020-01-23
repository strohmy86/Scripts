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

# This script will run NDSrepair on a selected server and report any errors

import sys
import time
import paramiko
import argparse


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
    print(Color.DARKCYAN + '\n')
    print('*********************************')
    print('*      NDScheck Utility         *')
    print('*                               *')
    print('*  Written and maintained by:   *')
    print('*        Luke Strohm            *')
    print('*    strohm.luke@gmail.com      *')
    print('*  https://github.com/strohmy86 *')
    print('*                               *')
    print('*********************************')
    print('\n' + Color.END)


def main(server, all_checks):
    # Specify private key file
    k = paramiko.RSAKey.from_private_key_file(
        '/Users/lstrohm/.ssh/Identityrsa')
    # Configure SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username='root', pkey=k)
    # Checks NDS time sync
    print(Color.YELLOW+'Checking NDS time sync on '+server+'...'+Color.END)
    stdin, stdout, stderr = client.exec_command('ndsrepair -T')
    for line in stdout:
        print(line.strip('\n'))
    print('\n')
    if all_checks is True:
        e = 'yes'
        time.sleep(5)
    elif all_checks is False:
        # Prompts user to run more tests
        e = input(Color.CYAN+'Would you like to continue checks? [Y/n]:  ' +
                  Color.END)
    if e == 'y' or e == 'yes' or e == '':
        print(Color.YELLOW+'Checking NDS replication status on '+server +
              '...'+Color.END)
        stdin, stdout, stderr = client.exec_command('ndsrepair -E')
        for line in stdout:
            print(line.strip('\n'))
        print('\n')
    elif e != 'y' or e != 'yes' or e != '':
        print(Color.GREEN+'Exiting.'+Color.END)
        client.close()
        sys.exit(0)
    if all_checks is True:
        n = 'yes'
        time.sleep(3)
    elif all_checks is False:
        # Prompts user to run the last test
        n = input(Color.CYAN+'Would you like to run the last check? [Y/n]:  ' +
                  Color.END)
    if n == 'y' or n == 'yes' or n == '':
        print(Color.YELLOW+'Checking NDS server status on '+server+'...' +
              Color.END)
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
        sys.exit(0)
    elif n != 'y' or n != 'yes' or n != '':
        print(Color.GREEN+'Exiting.'+Color.END)
        client.close()
        sys.exit(0)


# Starts the script.
parser = argparse.ArgumentParser(description='Script to check the NDS\
                                 status of a server.')
parser.add_argument('-a', '--all', default=False, action='store_const',
                    const=True, help='Run all checks without asking.')
parser.add_argument('server', metavar='Server', default='', type=str,
                    help='IP address or FQDN of server to run checks on')
args = parser.parse_args()
server = args.server
all_checks = args.all

cred()
main(server, all_checks)
