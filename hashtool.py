#!/usr/bin/env python3

# Just a simple script to create different types of hashes for a string.

import base64
import hashlib
import time

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

print("\n")
print(Color.DARKCYAN)
print("*********************************")
print("*      Hash Tool Utility        *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print(Color.END)
print("\n")

while True:
    print('\n')
    print(Color.PURPLE + 'Menu:' + Color.END)
    print('\n')
    print('1)  Create MD5 Hash')
    print('2)  Create SHA1 Hash')
    print('3)  Create SHA256 Hash')
    print('4)  Create SHA512 Hash')
    print('5)  Encode a String in base64')
    print('6)  Decode a base64 String')
    print('0)  Exit')
    print('\n')

    selection = input(Color.BOLD + 'Please Choose an Option: ' + Color.END)
    if selection == '1':
        string = input(Color.BOLD + 'Please input a string you would like to hash:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your hashed string is:  \n' + Color.END)
        print(hashlib.md5(str(string).encode('utf-8')).hexdigest())
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '2':
        string = input(Color.BOLD + 'Please input a string you would like to hash:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your hashed string is:  \n' + Color.END)
        print(hashlib.sha1(str(string).encode('utf-8')).hexdigest())
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '3':
        string = input(Color.BOLD + 'Please input a string you would like to hash:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your hashed string is:  \n' + Color.END)
        print(hashlib.sha256(str(string).encode('utf-8')).hexdigest())
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '4':
        string = input(Color.BOLD + 'Please input a string you would like to hash:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your hashed string is:  \n' + Color.END)
        print(hashlib.sha512(str(string).encode('utf-8')).hexdigest())
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '5':
        string = input(Color.BOLD + 'Please input a string you would like to encode:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your encoded string is:  \n' + Color.END)
        print(str(base64.standard_b64encode(string.encode()))[2:-1])
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '6':
        string = input(Color.BOLD + 'Please input a base64 string you would like to decode:  ' + Color.END)
        print('\n')
        print(Color.CYAN + 'Your decoded string is:  \n' + Color.END)
        print(str(base64.standard_b64decode(string.encode()))[2:-1])
        print('\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '0':
        break
    else:
        print(Color.RED + 'Unknown Option Selected!' + Color.END)
