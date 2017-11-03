#!/usr/bin/python2

import os
import time

print "*********************************"
print "*  GAM basic automation script  *"
print "*  Frontend to  GAM by jay0lee  *"
print "*                               *"
print "*  Written and maintained by:   *"
print "*        Luke Strohm            *"
print "*    strohm.luke@gmail.com      *"
print "*                               *"
print "*********************************"




while True:
    print '\n'
    print 'Menu:'
    print '\n'
    print '1)\tUser Information'
    print '2)\tExport List of All Users'
    print '3)\tActivate Suspended User'
    print '4)\tSuspend User'
    print "5)\tExport a List of a User's Drive Files"
    print "6)\tUpload a Local File To a User's Drive"
    print '0)\tExit'
    print '\n'

    selection=raw_input("Please Choose an Option: ")
    if selection =='1':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam info user " +username
        os.system(cmd)
        print '\n'
        time.sleep(2)
    elif selection =='2':
        cmd="~/bin/gam/gam print users allfields > Userlist.csv"
        os.system(cmd)
        print '\n'
        print "Userlist.csv saved."
        time.sleep(2)
    elif selection =='3':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam update user " +username + " suspended off"
        os.system(cmd)
        print '\n'
        time.sleep(2)
    elif selection =='4':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam update user " +username + " suspended on"
        os.system(cmd)
        print '\n'
        time.sleep(2)
    elif selection =='5':
        username=raw_input("Please enter a username: ")
        cmd="~/bin/gam/gam user " +username + " show filelist allfields > " +username + "-filelist.csv"
        os.system(cmd)
        print '\n'
        print "File list saved as " + username +"-filelist.csv."
        print '\n'
        time.sleep(2)
    elif selection =='6':
        username=raw_input("Please enter a username: ")
        filename=raw_input("Please enter the full path to the file you wish to upload: ")
        cmd="~/bin/gam/gam user " +username + " add drivefile localfile " +filename
        os.system(cmd)
        print '\n'
        print "File uploaded successfully"
        print '\n'
        time.sleep(2)
    elif selection =='0':
        break
    else:
        print "Unknown Option Selected!"
