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

# This is a python script to create a certificate request and then process it
# using the radius server.


import argparse
import pipes
import subprocess
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


def cred():
    print(Color.DARKCYAN+'\n' +
          '*********************************\n' +
          '*       CertGen Utility         *\n' +
          '*                               *\n' +
          '*  Written and maintained by:   *\n' +
          '*        Luke Strohm            *\n' +
          '*    strohm.luke@gmail.com      *\n' +
          '*  https://github.com/strohmy86 *\n' +
          '*                               *\n' +
          '*********************************\n' +
          '\n'+Color.END)


# Define global variables
path = '/media/nss/VOL1/shared/madhs01rad1/requests/'
parser = argparse.ArgumentParser(description='This is a python script\
                                 to create a certificate request and\
                                 then process it using the radius server.')
parser.add_argument('name', metavar='Name', default='',
                    type=str, help='Name of the PC that a certificate\
                     is being generated for.')
args = parser.parse_args()
name = args.name
# Specify private key file
k = paramiko.RSAKey.from_private_key_file('/home/lstrohm/.ssh/id_rsa')
# Configure SSH connections
fp = paramiko.SSHClient()
fp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
fp.connect('10.14.10.12', username='root', pkey=k)
rad = paramiko.SSHClient()
rad.set_missing_host_key_policy(paramiko.AutoAddPolicy())
rad.connect('10.14.0.26', username='root', pkey=k)


# Function to close all SSH connections and exit the script
def close():
    time.sleep(1)
    fp.close()
    rad.close()
    sys.exit()


# Initiates certificate request
def start(path, name):
    if name != '':  # Creates a certificate request if a PC name is given
        print(Color.YELLOW+'Creating certificate request for '+Color.BOLD
              + name + Color.END)
        stdin, stdout, stderr = fp.exec_command('touch ' + path + name)
        time.sleep(2)
        gen(path, name)
    elif name == '':  # If no name is given, start the function over
        print(Color.RED+'No machine name specified.'+Color.END)
        time.sleep(1)
        sys.exit(1)
    return


# Checks to make sure the request was successful, then runs the cert-gen script
def gen(path, name):
    resp = subprocess.call(  # Checks for the request file
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/id_rsa', 'root@10.14.10.12',
         'test -e ' + pipes.quote(path + name)])
    if resp == 0:  # If the file is present, runs the cert-gen script
        print(Color.CYAN+'Request created successfully, awaiting certificate',
              'generation...'+Color.END)
        stdin, stdout, stderr = rad.exec_command('/root/certgen/cert-gen')
        time.sleep(3)
        certcheck(path, name)
    elif resp != 0:  # If request file is missing, recommends trying again
        print(Color.RED+'Certificate request failed! Please try again.'
              + Color.END)
        close()
        sys.exit(1)


# Checks to see if the certificate was generated correctly
def certcheck(path, name):
    cert = '/media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12'
    # Checks to see if the certificate file was generated correctly
    gen1 = subprocess.call(
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/id_rsa', 'root@10.14.10.12',
         'test -e ' + pipes.quote(cert)])
    if gen1 == 0:  # If the certificate exists, exits cleanly
        print(Color.GREEN+'Certificate generated successfully!'+Color.END)
        close()
        sys.exit(0)
    # If certificate generation failed, prompts user to try again
    elif gen1 != 0:
        print(Color.RED+'Certificate generation failed!'+Color.END)
        close()
        sys.exit(1)


cred()
start(path, name)  # Initiates the script
