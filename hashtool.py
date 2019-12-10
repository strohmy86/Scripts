#!/usr/bin/env python3

# MIT License

# Copyright (c) 2019 Luke Strohm

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


print(Color.DARKCYAN + '\n')
print("*********************************")
print("*      Hash Tool Utility        *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*  https://github.com/strohmy86 *")
print("*                               *")
print("*********************************")
print('\n' + Color.END)


while True:
    print(Color.PURPLE + '\nMenu:\n' + Color.END)
    print('1)  Create MD5 Hash')
    print('2)  Create SHA1 Hash')
    print('3)  Create SHA256 Hash')
    print('4)  Create SHA512 Hash')
    print('5)  Encode a String in base64')
    print('6)  Decode a base64 String')
    print('\n0)  Exit\n')
    selection = input(Color.BOLD + 'Please Choose an Option: ' + Color.END)
    if selection == '1':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour hashed string is:  \n' + Color.END)
        print(hashlib.md5(str(string).encode('utf-8')).hexdigest(), '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '2':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour hashed string is:  \n' + Color.END)
        print(hashlib.sha1(str(string).encode('utf-8')).hexdigest(), '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '3':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour hashed string is:  \n' + Color.END)
        print(hashlib.sha256(str(string).encode('utf-8')).hexdigest(), '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '4':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour hashed string is:  \n' + Color.END)
        print(hashlib.sha512(str(string).encode('utf-8')).hexdigest(), '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '5':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour encoded string is:  \n' + Color.END)
        print(str(base64.standard_b64encode(string.encode()))[2:-1], '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '6':
        string = input(Color.BOLD + 'Please input a string you would like to' +
                       ' hash:  ' + Color.END)
        print(Color.CYAN + '\nYour decoded string is:  \n' + Color.END)
        print(str(base64.standard_b64decode(string.encode()))[2:-1], '\n')
        time.sleep(1)
        input(Color.GREEN + 'Press Enter to continue...' + Color.END)
    elif selection == '0':
        break
    else:
        print(Color.RED + 'Unknown Option Selected!' + Color.END)
