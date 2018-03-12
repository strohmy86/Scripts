#!/usr/bin/python


import ipaddress
import os
import time
from subprocess import Popen, DEVNULL

print("*********************************")
print("*      Pingsweep script         *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*                               *")
print("*********************************")
print("\n")
# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24):  ")
net = net_addr.replace(".", "_")
net = net.replace("/", "-")

# Ask user if they want the list exported to a file
file = input("Do you want to export the list to a text file? [y/N]:  ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

p = {} # ip -> process
for n in range(len(all_hosts)): # start ping process
    ip = str(all_hosts[n])
    p[ip] = Popen(['ping', '-n', '-c1', '-w1', ip], stdout=DEVNULL)

t = [] # List for active IP addresses 
while p:
    for ip, proc in p.items():
        if proc.poll() is not None: # ping finished
            del p[ip] # remove from the process list
            if proc.returncode == 0 and (file == "no" or file == "n" or file == ""):
                print('%s active' % ip)
                t.append(ip)
            elif proc.returncode == 0 and (file == "yes" or file == "y"):
                f = open('ActiveIps-'+net+'.txt','a')
                f.write('%s\n' % ip)
                f.close()
            #else:
            #    print('%s error' % ip)
            break

# Count total number of active IP addresses
if file == "yes" or file == "y":
    fr = open('ActiveIps-'+net+'.txt','r')
    total = len(fr.readlines())
    fr.close()
    fw = open('ActiveIps-'+net+'.txt','a')
    fw.write("Total Active Devices: %s" % total)
    fw.close()
    print("Saved list to ActiveIps-"+net+".txt")
elif file == "no" or file == "n" or file == "":
    print("Total Active Devices: %s" % len(t))
