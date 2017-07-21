#!/usr/bin/python

import ipaddress
import os
import time
from subprocess import Popen, DEVNULL

# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

p = {} # ip -> process
for n in range(len(all_hosts)): # start ping process
    ip = str(all_hosts[n])
    p[ip] = Popen(['ping', '-n', '-c1', '-w1', ip], stdout=DEVNULL)

while p:
    for ip, proc in p.items():
        if proc.poll() is not None: # ping finished
            del p[ip] # remove from the process list
            if proc.returncode == 0:
                print('%s active' % ip)
            #elif proc.returncode == 1:
            #    print('%s no response' % ip)
            #else:
            #    print('%s error' % ip)
            break
