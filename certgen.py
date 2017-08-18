#!/usr/bin/python

## This is a python script to create a certificate request and then process it using the radius server.

import sys
import time
import paramiko
import subprocess
import pipes

k = paramiko.RSAKey.from_private_key_file('/home/lstrohm/.ssh/Identityrsa') ## Specify private key file

## Configure SSH connections
fp = paramiko.SSHClient()
fp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
fp.connect('10.14.0.20', username='root', pkey = k)

rad = paramiko.SSHClient()
rad.set_missing_host_key_policy(paramiko.AutoAddPolicy())
rad.connect('10.14.0.26', username='root', pkey = k)

## Function to close all SSH connections and exit the script
def close():
    time.sleep(1)
    fp.close()
    rad.close()
    sys.exit()

def start():
    global name
    name = input("What is the name of the machine?  ") # First we need the machine name
    global path
    path = path + name
    ## Creates a certificate request if a PC name is given
    if name != '':
        print("Creating certificate request for " + name)
        stdin, stdout, stderr = fp.exec_command('touch ' + path)
        time.sleep(2)
    elif name == '':
        print('No machine name specified.')
        time.sleep(1)
        start()

path = '/media/nss/VOL1/shared/madhs01rad1/requests/'
name = ''

start()

## Checks to make sure the request was successful, then runs the cert-gen script
def gen():
    global path
    global name
    resp = subprocess.call(
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.0.20', 'test -e ' + pipes.quote(path)])
    if resp  == 0:
        print('Request created sucessfully, awating certificate generation...')
        stdin, stdout, stderr = rad.exec_command('/root/certgen/cert-gen')
        time.sleep(3)
    elif resp != 0:
        again = input('Certificate request failed! Would you like to try again? [Y/n]  ')
        if again == 'y' or again == 'yes' or again == '':
            gen()
            certcheck()
        elif again == 'n' or again == 'no':
            print('Exiting...')
            close()
        else:
            print('Error!')
            close()
gen()

## Checks to see if the certificate was generated correctly
def certcheck():
    global path
    global name
    cert = '/media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12'
    gen = subprocess.call(
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.0.20', 'test -e ' + pipes.quote(cert)])
    if gen == 0:
        again = input('Certificate generated sucessfully! Would you like to generate another certificate? [y/N]  ')
        if again == 'y' or again == 'yes':
            time.sleep(1)
            name = ''
            start()
            gen()
            certcheck()
        elif again == 'n' or again == 'no' or again == '':
            print('Exiting...')
            close()
        else:
            print('Error!')
            close()
    elif gen != 0:
        tryAgain = input('Certificate generation failed. Would you like to try again? [Y/n]  ')
        if tryAgain == 'y' or tryAgain == 'yes' or tryAgain == '':
            time.sleep(1)
            resp = subprocess.call(
                ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.0.20', 'test -e ' + pipes.quote(path)])
            if resp == 0:
                gen()
                certcheck()
            elif resp != 0:
                start()
                gen()
                certcheck()
        elif tryAgain == 'n' or tryAgain =='no':
            print('Exiting...')
            close()
        else:
            print('Error!')
            close()
certcheck()
