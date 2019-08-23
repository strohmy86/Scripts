#!/usr/bin/env python3

import socket

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

print(Color.DARKCYAN+"\n")
print("*********************************")
print("*    Port Checking script       *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n"+Color.END)

ip = input(Color.BOLD+"Enter the IP address: "+Color.END)
port = eval(input(Color.BOLD+"Enter port number: "+Color.END))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock.connect_ex((ip, port)):
    print(Color.RED+"\nPort", port, "is closed"+Color.END)
else:
    print(Color.GREEN+"\nPort", port, "is open"+Color.END)
