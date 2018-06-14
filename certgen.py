#!/usr/bin/env python3

# This is a python script to create a certificate request and then process it using the radius server.

import sys
import time
import paramiko
import subprocess
import pipes


def cred():

    print("\n")
    print("*********************************")
    print("*       CertGen Utility         *")
    print("*                               *")
    print("*  Written and maintained by:   *")
    print("*        Luke Strohm            *")
    print("*    strohm.luke@gmail.com      *")
    print("*                               *")
    print("*********************************")
    print("\n")


# Specify private key file
k = paramiko.RSAKey.from_private_key_file('/home/lstrohm/.ssh/Identityrsa')

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
    name = input("What is the name of the machine?  ")
    if name != '':  # Creates a certificate request if a PC name is given
        print("Creating certificate request for " + name)
        stdin, stdout, stderr = fp.exec_command('touch ' + path + name)
        time.sleep(2)
        gen()
    elif name == '':  # If no name is given, start the function over
        print('No machine name specified.')
        time.sleep(1)
        start()
    return


# Checks to make sure the request was successful, then runs the cert-gen script
def gen():
    global path
    global name
    resp = subprocess.call(  # Checks for the request file
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(path + name)])
    if resp  == 0:  # If the file is present, runs the cert-gen script
        print('Request created successfully, awaiting certificate generation...')
        stdin, stdout, stderr = rad.exec_command('/root/certgen/cert-gen')
        time.sleep(3)
        certcheck()
    elif resp != 0:  # If request file is missing, prompts to try again
        again = input('Certificate request failed! Would you like to try again? [Y/n]  ')
        if again == 'y' or again == 'yes' or again == '':  # If user wants to try again, the gen() function is restarted
            gen()
        elif again == 'n' or again == 'no':  # exits the script if user inputs n or no
            print('Exiting...')
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print('Error!')
            close()
    return


# Checks to see if the certificate was generated correctly
def certcheck():
    global path
    global name
    cert = '/media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12'
    gen1 = subprocess.call(  # Checks to see if the certificate file was generated correctly
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(cert)])
    if gen1 == 0:  # If the certificate exists, prompts user if they want to generate another
        again = input('Certificate generated successfully! Would you like to generate another certificate? [y/N]  ')
        if again == 'y' or again == 'yes':  # If yes, the script starts from the beginning
            time.sleep(1)
            start()
        elif again == 'n' or again == 'no' or again == '':  # If no, the script exits
            print('Exiting...')
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print('Error!')
            close()
    elif gen1 != 0:  # If certificate generation failed, prompts user to try again
        tryagain = input('Certificate generation failed. Would you like to try again? [Y/n]  ')
        if tryagain == 'y' or tryagain == 'yes' or tryagain == '':  # If user inputs yes, checks for existing request
            time.sleep(1)
            resp = subprocess.call(
                ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.10.12', 'test -e ' + pipes.quote(path + name)])
            if resp == 0:  # If request file exists, runs the gen() function
                gen()
            elif resp != 0:  # If the request does not exist, starts the script from the beginning
                start()
        elif tryagain == 'n' or tryagain == 'no':  # If user inputs no, exits the program
            print('Exiting...')
            close()
        else:  # If anything other than an input above is given, the script errors out and exits
            print('Error!')
            close()
    return


cred()
start()  # Initiates the script
