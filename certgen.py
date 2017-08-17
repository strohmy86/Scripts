#!/usr/bin/python

## This is a simple python script to create a certificate request and then process it using the radius server.

import sys
import time
import paramiko
import subprocess
import pipes

k = paramiko.RSAKey.from_private_key_file('/home/lstrohm/.ssh/Identityrsa')

fp = paramiko.SSHClient()
fp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
fp.connect('10.14.0.20', username='root', pkey = k)

rad = paramiko.SSHClient()
rad.set_missing_host_key_policy(paramiko.AutoAddPolicy())
rad.connect('10.14.0.26', username='root', pkey = k)

name = input("What is the name of the machine?  ") # First we need the machine name
path = '/media/nss/VOL1/shared/madhs01rad1/requests/' + name
cert = '/media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12'

stdin, stdout, stderr = fp.exec_command('rm -f /media/nss/VOL1/shared/madhs01rad1/certs/' + name + '_cert.p12') ## Deletes old certificate file

## Creates a certificate request if a PC name is given
if name != '':
    print("Creating certificate request for " + name)
    stdin, stdout, stderr = fp.exec_command('touch ' + path)
    time.sleep(2)
elif name == '':
    print('No machine name specified. Exiting...')
    time.sleep(1)
    sys.exit()

## Checks to make sure the request was successful, then runs the cert-gen script
resp = subprocess.call(
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.0.20', 'test -e ' + pipes.quote(path)])
if resp  == 0:
    print('Request created, awating certificate generation...')
    stdin, stdout, stderr = rad.exec_command('/root/certgen/cert-gen')
    time.sleep(3)
elif resp != 0:
    print('Certificate request failed! Exiting...')
    time.sleep(1)
    sys.exit()

## Checks to see if the certificate was generated correctly
gen = subprocess.call(
        ['ssh', '-q', '-i', '/home/lstrohm/.ssh/Identityrsa', 'root@10.14.0.20', 'test -e ' + pipes.quote(cert)])

if gen == 0:
    print('Certificate generated sucessfully!')
    time.sleep(2)
    fp.close()
    rad.close()
    sys.exit()
elif gen != 0:
    print('Certificate generation failed. Exiting...')
    time.sleep(1)
    fp.close()
    rad.close()
    sys.exit()
