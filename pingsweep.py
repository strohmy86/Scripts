#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Luke Strohm

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


import argparse
import ipaddress
from subprocess import DEVNULL, Popen


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def cred():
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "*      Pingsweep script         *\n"
        + "*                               *\n"
        + "*  Written and maintained by:   *\n"
        + "*        Luke Strohm            *\n"
        + "*    strohm.luke@gmail.com      *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*                               *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def main(net_addr, file):
    net = net_addr.replace(".", "_")
    net = net.replace("/", "-")
    # Create the network
    ip_net = ipaddress.ip_network(net_addr)
    # Get all hosts on that network
    all_hosts = list(ip_net.hosts())
    p = {}  # ip -> process
    for n in range(len(all_hosts)):  # start ping process
        ip = str(all_hosts[n])
        p[ip] = Popen(
            ["ping", "-n", "-c", "1", "-w", "2", ip],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
    t = []  # List for active IP addresses
    if file is True:
        f = open("/home/lstrohm/ActiveIps-" + net + ".txt", "w")
        f.close()
    while p:
        for ip, proc in p.items():
            if proc.poll() is not None:  # ping finished
                del p[ip]  # remove from the process list
                if proc.returncode == 0 and file is False:
                    print(f"{ip} active")
                    t.append(ip)
                elif proc.returncode == 0 and file is True:
                    f = open("/home/lstrohm/ActiveIps-" + net + ".txt", "a")
                    f.write(f"{ip}\n")
                # else:
                #    print('%s error' % ip)
                break
    # Count total number of active IP addresses
    if file is True:
        fr = open("/home/lstrohm/ActiveIps-" + net + ".txt", "r")
        total = len(fr.readlines())
        fr.close()
        fw = open("/home/lstrohm/ActiveIps-" + net + ".txt", "a")
        fw.write(f"Total Active Devices: {total}")
        fw.close()
        print(
            Color.CYAN
            + "Saved list to ~/ActiveIps-"
            + net
            + ".txt"
            + Color.END
        )
    elif file is False:
        print(Color.YELLOW + f"Total Active Devices: {len(t)}" + Color.END)


# Starts the script.
parser = argparse.ArgumentParser(description="Script ping sweep a subnet")
parser.add_argument(
    "-f",
    "--file",
    default=False,
    action="store_const",
    const=True,
    help="Write results to a text file.",
)
parser.add_argument(
    "net",
    metavar="Network Subnet",
    default="",
    type=str,
    help="network address in CIDR format (ex.192.168.1.0/24)",
)
args = parser.parse_args()
net_addr = args.net
file = args.file

cred()
main(net_addr, file)
