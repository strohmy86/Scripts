#!/usr/bin/env python3

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
