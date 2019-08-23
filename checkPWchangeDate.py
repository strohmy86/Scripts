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

from datetime import datetime, timedelta
import time


print("\n")
print("*********************************")
print("*    Utility to Check When      *")
print("*    A Password Was Changed     *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n")


class color:
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


def start():
    pwexp = input("What is the Password expiration date? (mm-dd-yyyy):  ")
    chgDate = datetime.strptime(pwexp, '%m-%d-%Y') - timedelta(days=90)
    dateStr = chgDate.strftime('%m-%d-%Y')
    print("The user changed their password on " + color.RED + dateStr + color.END)
    time.sleep(2)
    again()

def again():
    again = input("Would you like to check another password? [y/N]:  ")

    if again == 'y' or again == 'yes':  # If yes, the script starts from the beginning
        time.sleep(1)
        start()
    elif again == 'n' or again == 'no' or again == '':  # If no, the script exits
        print('Exiting...')
        time.sleep(1)
        exit()
    else:  # If anything other than an input above is given, the script errors out and exits
        print('Error!')
        time.sleep(1)
        exit()


start()
