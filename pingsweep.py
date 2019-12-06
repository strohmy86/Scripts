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

import ipaddress
from subprocess import Popen, DEVNULL


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
print("*      Pingsweep script         *")
print("*                               *")
print("*  Written and maintained by:   *")
print("*        Luke Strohm            *")
print("*    strohm.luke@gmail.com      *")
print("*  https://github.com/strohmy86 *")
print("*                               *")
print("*********************************")
print("\n"+Color.END)


# Prompt the user to input a network address
net_addr = input(Color.BOLD+"Enter a network address in CIDR format"+\
                "(ex.192.168.1.0/24):  "+Color.END)
net = net_addr.replace(".", "_")
net = net.replace("/", "-")
# Ask user if they want the list exported to a file
file = input(Color.BOLD+"Do you want to export the list to a text file? "+\
            "[y/N]:  "+Color.END)
# Create the network
ip_net = ipaddress.ip_network(net_addr)
# Get all hosts on that network
all_hosts = list(ip_net.hosts())
p = {}  # ip -> process
for n in range(len(all_hosts)):  # start ping process
    ip = str(all_hosts[n])
    p[ip] = Popen(['ping', '-n', '-c1', '-w1', ip], stdout=DEVNULL)
t = []  # List for active IP addresses
while p:
    for ip, proc in p.items():
        if proc.poll() is not None:  # ping finished
            del p[ip]  # remove from the process list
            if proc.returncode == 0 and (file == "no" or file == "n" or \
                file == ""):
                print('%s active' % ip)
                t.append(ip)
            elif proc.returncode == 0 and (file == "yes" or file == "y"):
                f = open('ActiveIps-'+net+'.txt', 'a')
                f.write('%s\n' % ip)
                f.close()
            # else:
            #    print('%s error' % ip)
            break
# Count total number of active IP addresses
if file == "yes" or file == "y":
    fr = open('ActiveIps-'+net+'.txt', 'r')
    total = len(fr.readlines())
    fr.close()
    fw = open('ActiveIps-'+net+'.txt', 'a')
    fw.write("Total Active Devices: %s" % total)
    fw.close()
    print(Color.CYAN+"Saved list to ActiveIps-"+net+".txt"+Color.END)
elif file == "no" or file == "n" or file == "":
    print(Color.YELLOW+"Total Active Devices: %s" % len(t)+Color.END)
