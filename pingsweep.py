#!/usr/bin/python

# Import modules
import multiprocessing
import subprocess
import ipaddress
import os

# Prompt the user to input a network address
net_addr = input("Enter a network address in CIDR format(ex.192.168.1.0/24): ")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# For each IP address in the subnet, 
# run the ping command with subprocess.popen interface
for i in range(len(all_hosts)):
    output = subprocess.Popen(['ping', '-c', '1', '-w', '1', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()[0]
    
    if "Destination host unreachable" in output.decode('utf-8'):
        print(str(all_hosts[i]), "is Offline")
    elif "Request timed out" in output.decode('utf-8'):
        print(str(all_hosts[i]), "is Offline")
    elif "100% packet loss" in output.decode('utf-8'):
        print(str(all_hosts[i]), "is Offline")
    else:
        print(str(all_hosts[i]), "is Online")
