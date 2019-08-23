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

# This is a python script to create a certificate request and then process it using the radius server.

import sys
import time
import paramiko
import subprocess
import pipes

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

    print(Color.DARKCYAN+"\n")
    print("*********************************")
    print("*       CertGen Utility         *")
    print("*                               *")
    print("*  Written and maintained by:   *")
    print("*        Luke Strohm            *")
    print("*    strohm.luke@gmail.com      *")
    print("*                               *")
    print("*********************************")
    print("\n"+Color.END)


# Specify private key file
k = paramiko.RSAKey.from_private_key_file('/Users/LStrohm/.ssh/Identityrsa')

# Configure SSH connections
fp = paramiko.SSHClient()
fp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
fp.connect('10.14.10.12', username='root', pkey=k)

rad = paramiko.SSHClient()
rad.set_missing_host_key_policy(paramiko.AutoAddPolicy())
rad.connect('10.14.0.26', username='root', pkey=k)

# Define global variables
path = '/media/nss/VOL1/shared/madhs01rad1/requests/'
name = ''


# Function to close all SSH connections and exit the script
def close():
    time.sleep(1)
    fp.close()
    rad.close()
    sys.exit()


# Gathers PC name and initiates certificate request
def start():
    global name
    global path
    name = input(Color.BOLD+"What is the name of the machine?  "+Color.END)
    if name != '':  # Creates a certificate request if a PC name is given
        print(Color.YELLOW+"Creating certificate request for "+Color.BOLD + name + Color.END)
        stdin, stdout, stderr = fp.exec_command('touch ' + path + name)
        time.sleep(2)
        gen()
    elif name == '':  # If no name is given, start the function over
        print(Color.RED+'No machine name specified.'+Color.END)
        time.sleep(1)
        start()
    return


# Checks to make sure the request was successful, then runs the cert-gen script
def gen():
    global path
    global name
    resp = subprocess.call(  # Checks for the request file
        ['ssh', '-q', '-i', '/Users/LStrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(path + name)])
    if resp  == 0:  # If the file is present, runs the cert-gen script
        print(Color.CYAN+'Request created successfully, awaiting certificate generation...'+Color.END)
        stdin, stdout, stderr = rad.exec_command('/root/certgen/cert-gen')
        time.sleep(3)
        certcheck()
    elif resp != 0:  # If request file is missing, prompts to try again
        again = input(Color.RED+'Certificate request failed! Would you like to try again? [Y/n]  '+Color.END)
        if again == 'y' or again == 'yes' or again == '':  # If user wants to try again, the gen() function is restarted
            gen()
        elif again == 'n' or again == 'no':  # exits the script if user inputs n or no
            print(Color.GREEN+'Exiting...'+Color.END)
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print(Color.RED+'Error!'+Color.END)
            close()
    return


# Checks to see if the certificate was generated correctly
def certcheck():
    global path
    global name
    cert = '/media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12'
    gen1 = subprocess.call(  # Checks to see if the certificate file was generated correctly
        ['ssh', '-q', '-i', '/Users/LStrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(cert)])
    if gen1 == 0:  # If the certificate exists, prompts user if they want to generate another
        again = input(Color.GREEN+'Certificate generated successfully! Would you like to generate another certificate? [y/N]  '+Color.END)
        if again == 'y' or again == 'yes':  # If yes, the script starts from the beginning
            time.sleep(1)
            start()
        elif again == 'n' or again == 'no' or again == '':  # If no, the script exits
            print(Color.GREEN+'Exiting...'+Color.END)
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print(Color.RED+'Error!'+Color.END)
            close()
    elif gen1 != 0:  # If certificate generation failed, prompts user to try again
        tryagain = input(Color.RED+'Certificate generation failed. Would you like to try again? [Y/n]  '+Color.END)
        if tryagain == 'y' or tryagain == 'yes' or tryagain == '':  # If user inputs yes, checks for existing request
            time.sleep(1)
            resp = subprocess.call(
                ['ssh', '-q', '-i', '/Users/LStrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(path + name)])
            if resp == 0:  # If request file exists, runs the gen() function
                gen()
            elif resp != 0:  # If the request does not exist, starts the script from the beginning
                start()
        elif tryagain == 'n' or tryagain == 'no':  # If user inputs no, exits the program
            print(Color.GREEN+'Exiting...'+Color.END)
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print(Color.RED+'Error!'+Color.END)
            close()
    return


cred()
start()  # Initiates the script
