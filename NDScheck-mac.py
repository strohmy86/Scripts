#!/usr/bin/env python3

# This script will run NDSrepair on a selected server and report any errors

import sys
import time
import paramiko

print("*********************************")
print("*      NDScheck Utility         *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n")


def main(server):

    # Specify private key file
    k = paramiko.RSAKey.from_private_key_file('/Users/LStrohm/.ssh/Identityrsa')

    # Configure SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username='root', pkey=k)

    # Checks NDS time sync
    print('Checking NDS time sync...')
    stdin, stdout, stderr = client.exec_command('ndsrepair -T')
    for line in stdout:
        print(line.strip('\n'))
    print('\n')

    # Prompts user to run more tests
    e = input('Would you like to continue checks? [Y/n]:  ')
    if e == 'y' or e == 'yes' or e == '':
        print('Checking NDS replication status...')
        stdin, stdout, stderr = client.exec_command('ndsrepair -E')
        for line in stdout:
            print(line.strip('\n'))
        print('\n')
    elif e != 'y' or e != 'yes' or e != '':
        print('Exiting.')
        client.close()
        menu()

    # Prompts user to run the last test
    n = input('Would you like to run the last check? [Y/n]:  ')
    if n == 'y' or n == 'yes' or n == '':
        print('Checking NDS server status...')
        stdin, stdout, stderr = client.exec_command('ndsrepair -N')
        time.sleep(1)
        stdin.write('\n')
        time.sleep(1)
        stdin.write('\n')
        time.sleep(1)
        stdin.write('q\n')
        stdin.flush()
        data = stdout.read().splitlines()
        for line in data:
            print(line)
        print('\n')
        input('Press Enter to continue...')
    elif n != 'y' or n != 'yes' or n != '':
        print('Exiting.')
        client.close()
        menu()


def menu():

    # Generate the menu.
    while True:
        print('\n')
        print('Menu:')
        print('\n')
        print('1)\tMADHS01FP1')
        print('2)\tMADHS01STAFF1')
        print('3)\tMADHS01STU1')
        print('4)\tMADHS01NS1')
        print('5)\tMADHS01NS2')
        print('6)\tMADHS01WEB1')
        print('7)\tMADHS01GW1')
        print('8)\tMADMS01FP1')
        print('9)\tMADEA01FP1')
        print('10)\tMADMI01FP1')
        print('11)\tMADSO01FP1')
        print('0)\tExit')
        print('\n')

        # Prompts user to select a menu item.
        selection = input('Please Choose a Server: ')

        # Sets the server variable based on menu selection then executes the main function.
        if selection == '1':
            server = '10.14.0.20'
            main(server)
        elif selection == '2':
            server = '10.14.10.12'
            main(server)
        elif selection == '3':
            server = '10.14.10.11'
            main(server)
        elif selection == '4':
            server = '10.14.0.4'
            main(server)
        elif selection == '5':
            server = '10.14.0.5'
            main(server)
        elif selection == '6':
            server = '10.14.0.22'
            main(server)
        elif selection == '7':
            server = '10.14.0.6'
            main(server)
        elif selection == '8':
            server = '10.14.48.10'
            main(server)
        elif selection == '9':
            server = '10.14.16.10'
            main(server)
        elif selection == '10':
            server = '10.14.40.10'
            main(server)
        elif selection == '11':
            server = '10.14.32.10'
            main(server)
        elif selection == '0':
            sys.exit()
        else:
            print('Unknown Option Selected!')

# Starts the script.


menu()
