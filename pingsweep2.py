#!/bin/env python3

import argparse
import ipaddress
import subprocess


def replace_chars(network_address):
    network_address = network_address.replace(".", "_")
    network_address = network_address.replace("/", "-")
    return network_address


def ping_hosts_on_network(network_address):
    network = ipaddress.ip_network(network_address)
    processes = {}
    for host in network.hosts():
        ip = str(host)
        processes[ip] = subprocess.Popen(
            ["ping", "-n", "-c", "1", "-w", "2", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    active_ips = []
    while processes:
        for ip, process in processes.items():
            if process.poll() is not None:
                del processes[ip]
                if process.returncode == 0:
                    active_ips.append(ip)
                break
    return active_ips


def write_to_file(file_path, active_ips):
    with open(file_path, "w") as f:
        for ip in active_ips:
            f.write(f"{ip}\n")


def count_active_ips(file_path):
    with open(file_path, "r") as f:
        total = len(f.readlines())
    with open(file_path, "a") as f:
        f.write(f"Total Active Devices: {total}")
    return total


def main(network_address, write_to_file):
    #network_address = replace_chars(network_address)
    active_ips = ping_hosts_on_network(network_address)
    if write_to_file:
        file_path = f"/home/lstrohm/ActiveIps-{network_address}.txt"
        write_to_file(file_path, active_ips)
        total = count_active_ips(file_path)
        print(f"Saved list to {file_path}\nTotal Active Devices: {total}")
    else:
        print(f"Total Active Devices: {len(active_ips)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script ping sweep a subnet")
    parser.add_argument("-f", "--file", default=False, action="store_const", const=True, help="Write results to a text file.")
    parser.add_argument("network_address", metavar="Network Subnet", default="", type=str, help="network address in CIDR format (ex.192.168.1.0/24)")
    args = parser.parse_args()
    main(args.network_address, args.file)
