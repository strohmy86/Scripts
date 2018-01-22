#!/usr/bin/python2

import socket
ip = raw_input("Enter the IP address: ")
port = input("Enter port number: ")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if sock.connect_ex((ip,port)):
    print "Port", port, "is closed"
else:
    print "Port", port, "is open"
