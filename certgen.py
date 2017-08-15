#!/usr/bin/python

## This is a simple python script to create an empty file and copy it to the cert request directory for processing by the radius server.

import os
import subprocess
import pipes

name = input("What is the name of the machine?  ") # First we need the machine name

print("Creating certificate request for " + name)

os.system("touch /tmp/" + name) # This creates the request locally

os.system("scp /tmp/" + name + " root@10.14.0.20:/media/nss/VOL1/shared/madhs01rad1/requests/") # This copies the local file to the proper directory on the server

ssh_host = 'root@10.14.0.20'
path = '/media/nss/VOL1/shared/madhs01rad1/requests/' + name

resp = subprocess.call( # Check for existence of request file on remote server
        ['ssh', ssh_host, 'test -e ' + pipes.quote(path)]) 

if resp == 0:
    print("Certificate request succedssfull. Please wait up to 10 minutes before attempting to import.")
else:
    print("Cannot find " + name + "in requests directory. Please manually check.")

os.system("rm -f /tmp/" + name) # Deletes the local file
