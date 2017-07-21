#!/usr/bin/python2

import os


menu = {}
menu['1']="User Information"
menu['2']="Export List of All Users"
menu['3']="Activate Suspended User"
menu['4']="Suspend User"
menu['5']="Export a List of a User's Drive Files"
menu['6']="Upload a File To a User's Drive"
menu['0']="Exit"
while True:
    options=menu.keys()
    options.sort()
    for entry in options:
      print entry, menu[entry]

    selection=raw_input("Please Choose an Option: ")
    if selection =='1':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam info user " +username
        os.system(cmd)
    elif selection =='2':
        cmd="~/bin/gam/gam print users allfields > Userlist.csv"
        os.system(cmd)
        print "Userlist.csv saved."
    elif selection =='3':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam update user " +username + " suspended off"
        os.system(cmd)
    elif selection =='4':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam update user " +username + " suspended on"
        os.system(cmd)
    elif selection =='5':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam user " +username + " show filelist allfields > " +username + "-filelist.csv"
        os.system(cmd)
        print "File list saved as " + username +"-filelist.csv."
    elif selection =='6':
        username=raw_input("Please enter a username: ")
        filename=raw_input("Please enter the full path to the file you wish to upload: ")
        cmd="~/bin/gam/gam user " +username + " add drivefile localfile " +filename
        os.system(cmd)
        print "File uploaded successfully"
    elif selection =='0':
        break
    else:
        print "Unknown Option Selected!"
