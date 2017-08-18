#!/usr/bin/python

#This script will run NDSrepair on madhs01fp1 and report any errors

import sys
import time
import paramiko

## Specify private key file
k = paramiko.RSAKey.from_private_key_file('/home/lstrohm/.ssh/Identityrsa')

## Configure SSH connection
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.14.0.20', username='root', pkey = k)

## Checks NDS time sync
print('Checking NDS time sync...')
stdin, stdout, stderr = client.exec_command('ndsrepair -T')
for line in stdout:
    print(line.strip('\n'))


## Prompts user to run more tests
e = input('Would you like to continue checks? [Y/n]:  ')
if e == 'y' or e == 'yes' or e == '':
    print('Checking NDS replication status...')
    stdin, stdout, stderr = client.exec_command('ndsrepair -E')
    for line in stdout:
        print(line.strip('\n'))
elif e != 'y' or e != 'yes' or e != '':
    print('Exiting.')
    sys.exit()


## Prompts user to run the last test
n = input('Would you like to run the last check? [Y/n]:  ')
if n == 'y' or n == 'yes' or n == '':
    print('Checking NDS server status...')
    stdin, stdout, stderr = client.exec_command('ndsrepair -N')
    time.sleep(1)
    stdin.write('\n')
    time.sleep(1)
    stdin.write('q\n')
    stdin.flush()
    data = stdout.read().splitlines()
    for line in data:
        print(line)
elif n != 'y' or n != 'yes' or n != '':
    print('Exiting.')
    sys.exit()

client.close()
