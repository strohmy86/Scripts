#!/usr/bin/env python3

# Just a simple script to create different types of hashes for a string.

import os
import time

print("\n")
print("*********************************")
print("*      Hash Tool Utility        *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n")

while True:
    print('\n')
    print('Menu:')
    print('\n')
    print('1)\tCreate MD5 Hash')
    print('2)\tCreate SHA1 Hash')
    print('3)\tCreate SHA256 Hash')
    print('4)\tCreate SHA512 Hash')
    print('5)\tEncode a String in base64')
    print('6)\tDecode a base64 String')
    print('0)\tExit')
    print('\n')

    selection = input('Please Choose an Option: ')
    if selection == '1':
        string = input('Please input a string you would like to hash:  ')
        cmd = 'echo -n "'+string+'" | md5sum | cut -d " " -f1'
        print('\n')
        print('Your hashed string is:  \n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '2':
        string = input('Please input a string you would like to hash:  ')
        cmd = 'echo -n "'+string+'" | sha1sum | cut -d " " -f1'
        print('\n')
        print('Your hashed string is:  \n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '3':
        string = input('Please input a string you would like to hash:  ')
        cmd = 'echo -n "'+string+'" | sha256sum | cut -d " " -f1'
        print('\n')
        print('Your hashed string is:  \n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '4':
        string = input('Please input a string you would like to hash:  ')
        cmd = 'echo -n "'+string+'" | sha512sum | cut -d " " -f1'
        print('\n')
        print('Your hashed string is:  \n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '5':
        string = input('Please input a string you would like to encode:  ')
        cmd = 'echo -n "'+string+'" | base64'
        print('\n')
        print('Your encoded string is:\n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '6':
        string = input('Please input a base64 string you would like to decode:  ')
        cmd = 'echo -n '+string+' | base64 -d'
        print('\n')
        print('Your decoded string is:\n')
        os.system(cmd)
        print('\n')
        time.sleep(1)
        input('Press Enter to continue...')
    elif selection == '0':
        break
    else:
        print('Unknown Option Selected!')