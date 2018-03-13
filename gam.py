#!/usr/bin/env python

import os
import time
import sys


def cred():

    print('\n')
    print("*********************************")
    print("*  GAM basic automation script  *")
    print("*  Frontend to  GAM by jay0lee  *")
    print("*                               *")
    print("*  Written and maintained by:   *")
    print("*        Luke Strohm            *")
    print("*    strohm.luke@gmail.com      *")
    print("*                               *")
    print("*********************************")
    print('\n')


def main_menu():  # Main Menu
    while True:
        print('\n')
        print('Menu:')
        print('\n')
        print('1)\tUser Management')
        print('2)\tCalendar Management')
        print('3)\tDrive Management')
        print('4)\tGroup Management')
        print('5)\tClassroom Management')
        print('6)\tDevice Management')
        print('0)\tExit')
        print('\n')

        selection1 = input('Please Choose an Option: ')
        if selection1 == '0':
            sys.exit()
        elif selection1 == '1':
            users()
        elif selection1 == '2':
            calendar()
        elif selection1 == '3':
            drive()
        elif selection1 == '4':
            groups()
        elif selection1 == '5':
            classroom()
        elif selection1 == '6':
            devices()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def users():  # User ManagementMain Menu
    while True:
        print('\n')
        print('User Management Menu:')
        print('\n')
        print('1)\tUser Information')
        print('2)\tExport List of All Users')
        print('3)\tActivate Suspended User')
        print('4)\tSuspend User')
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            username = input("Please enter a username: ")
            cmd = "~/bin/gam/gam info user " + username
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            cmd = "~/bin/gam/gam print users allfields > Userlist.csv"
            os.system(cmd)
            print('\n')
            print("Userlist.csv saved.")
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            username = input("Please enter a username: ")
            cmd = "~/bin/gam/gam update user " + username + " suspended off"
            cmd2 = "~/bin/gam/gam info user " + username
            os.system(cmd)
            time.sleep(2)
            os.system(cmd2)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '4':
            username = input("Please enter a username: ")
            cmd = "~/bin/gam/gam update user " + username + " suspended on"
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def calendar():  # Calendar Management Main Menu
    while True:
        print('\n')
        print('Calendar Management Menu:')
        print('\n')
        print('1)\tShow Permissions For a Calendar')
        print("2)\tAdd or Remove Calendar Permissions")
        print('3)\tDelete a Calendar Event')
        print("4)\tList a User's Calendar(s)")
        print("5)\tDelete a User's Calendar (Cannot delete default calendar)")
        print("6)\tAdd a Calendar to a User")
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            cal = input('Please enter a Google Calendar email address: ')
            cmd = '~/bin/gam/gam calendar ' + cal + ' showacl'
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            cal = input('Please enter a Google Calendar email address: ')
            ar = input('What would you like to do? [add | remove] ')
            user = input('User to add to/remove from the Calendar: ')
            if ar == 'add' or ar == 'Add' or ar == 'a':
                act = input('What permission would you like to grant? [read | edit | owner] ')
                if act == 'read' or act == 'r' or act == 'Read':
                    cmd = '~/bin/gam/gam calendar ' + cal + ' add read ' + user
                    os.system(cmd)
                    print('\n')
                    time.sleep(2)
                    input("Press ENTER to Continue...")
                    break
                elif act == 'edit' or act == 'editor' or act == 'e' or act == 'Edit':
                    cmd = '~/bin/gam/gam calendar ' + cal + ' add editor ' + user
                    os.system(cmd)
                    print('\n')
                    time.sleep(2)
                    input("Press ENTER to Continue...")
                    break
                elif act == 'owner' or act == 'own' or act == 'o' or act == 'Owner':
                    cmd = '~/bin/gam/gam calendar ' + cal + ' add owner ' + user
                    os.system(cmd)
                    print('\n')
                    time.sleep(2)
                    input("Press ENTER to Continue...")
                    break
                else:
                    print("Unknown Option Selected!")
                    print('\n')
                    time.sleep(2)
                    input("Press ENTER to Continue...")
            elif ar == 'rem' or ar == 'remove' or ar == 'r' or ar == 'Remove' or ar == 'Rem':
                cmd = '~/bin/gam/gam calendar ' + cal + ' delete user ' + user
                os.system(cmd)
                print('\n')
                time.sleep(2)
                input("Press ENTER to Continue...")
                break
            else:
                print("Unknown Option Selected!")
                print('\n')
                time.sleep(2)
                input("Press ENTER to Continue...")
        elif selection == '3':
            cal = input('Please enter a Google Calendar email address: ')
            ev = input('Enter the event ID: ')
            yn = input('Are you sure? THIS CANNOT BE UNDONE!! [y/N] ')
            if yn == '' or yn == 'N' or yn == 'n' or yn == 'no' or yn == 'No':
                break
            elif yn == 'y' or yn == 'Y' or yn == 'yes' or yn == 'Yes':
                cmd = '~/bin/gam/gam calendar ' + cal + ' deleteevent ' + ev + ' doit'
                os.system(cmd)
                print('\n')
                time.sleep(2)
                input("Press ENTER to Continue...")
                break
        elif selection == '4':
            user = input('Please enter a username: ')
            cmd = '~/bin/gam/gam user ' + user + ' show calendars'
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '5':
            user = input('Please enter a username: ')
            cal = input('Please enter a Google Calendar email address: ')
            cmd = '~/bin/gam/gam user ' + user + ' delete calendar ' + cal
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '6':
            user = input('Please enter a username: ')
            cal = input('Please enter a Google Calendar email address: ')
            cmd = '~/bin/gam/gam user ' + user + ' add calendar ' + cal + ' selected true hidden false'
            os.system(cmd)
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def drive():  # Drive Management Main Menu
    while True:
        print('\n')
        print('Drive Management Menu:')
        print('\n')
        print("1)\tExport a List of a User's Drive Files")
        print("2)\tUpload a Local File To a User's Drive")
        print("3)\tView a User's Team Drive(s)")
        print('4)\tCreate a Team Drive For a User')
        print("5)\tDelete a User's Team Drive")
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            username = input("Please enter a username: ")
            cmd = "~/bin/gam/gam user " + username + " show filelist allfields > " + username + "-filelist.csv"
            os.system(cmd)
            print('\n')
            print("File list saved as " + username + "-filelist.csv.")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            username = input("Please enter a username: ")
            filename = input("Please enter the full path to the file you wish to upload (Case Sensitive): ")
            cmd = "~/bin/gam/gam user " + username + " add drivefile localfile " + filename
            os.system(cmd)
            print('\n')
            print("File uploaded successfully")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            username = input("Please enter a username: ")
            cmd = '~/bin/gam/gam user ' + username + ' show teamdrives'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '4':
            user = input("Please enter a username: ")
            name = input('What is the name of the Team Drive? ')
            cmd = '~/bin/gam/gam user ' + user + ' add teamdrive ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '5':
            user = input("Please enter a username: ")
            dr_id = input('What is the Team Drive ID? (Not the name) ')
            cmd = '~/bin/gam/gam user ' + user + ' delete teamdrive ' + dr_id
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def groups():  # Groups Management Main Menu
    while True:
        print('\n')
        print('Group Management Menu:')
        print('\n')
        print('1)\tCreate a Group')
        print('2)\tRename a Group')
        print('3)\tAdd or Remove Group Member')
        print('4)\tUpdate User Role in a Group')
        print('5)\tGet Group Information')
        print('6)\tDelete a Group')
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")

        if selection == '1':
            name = input('What is the name of the group to be created? ')
            cmd = '~/bin/gam/gam create group ' + name + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            name = input('What is the email address of the group to be renamed? ')
            ren = input('What is the new name(email address) of the group? ')
            cmd = '~/bin/gam/gam update group ' + name + ' email ' + ren
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            name = input('What is the email address of the group?')
            ar = input('Add or Remove user? [add | remove] ')
            user = input('What user? ')
            if ar == 'add' or ar == 'a' or ar == 'Add' or ar == 'A':
                cmd = '~/bin/gam/gam update group ' + name + ' add member user ' + user
                os.system(cmd)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                break
            elif ar == 'remove' or ar == 'r' or ar == 'R' or ar == 'Remove' or ar == 'rem' or ar == 'Rem':
                cmd = '~/bin/gam/gam update group ' + name + ' remove user ' + user
                os.system(cmd)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                break
            else:
                print("Unknown Option Selected!")
                print('\n')
                time.sleep(2)
                input("Press ENTER to Continue...")
        elif selection == '4':
            name = input('What is the email address of the group?')
            user = input("What user's role will be modified? ")
            perm = input('New role to assign (Must be in Lower Case): [owner | member | manager] ')
            cmd = '~/bin/gam/gam update group ' + name + ' update ' + perm + ' user ' + user
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '5':
            name = input('What is the email address of the group?')
            cmd = '~/bin/gam/gam info group ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '6':
            name = input('What is the email address of the group?')
            cmd = '~/bin/gam/gam delete group ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def classroom():  # Classroom Management Main Menu
    while True:
        print('Classroom Management Main Menu:')
        print('\n')
        print('1)\tManage Courses')
        print('2)\tManage Course Participants')
        print('3)\tManage Guardians')
        print('4)\tReports')
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            classroom1()
        elif selection == '2':
            al = input('What is the course ID or alias? ')
            act = input('Do you want to Add or Remove? (Must be lower case) [add | remove] ')
            who = input('Is the person a student or a teacher? (Must be lower case) [student | teacher] ')
            user = input("What is the person's username? ")
            cmd = '~/bin/gam/gam course ' + al + ' ' + act + ' ' + who + ' ' + user + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            classroom3()
        elif selection == '4':
            classroom4()
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")
            break


def devices():  # Device Management Main Menu
    while True:
        print('\n')
        print('Chrome Device Management Main Menu:')
        print('\n')
        print('1)\tGet Device ID of a Chrome OS Device')
        print('2)\tUpdate Device Info')
        print('3)\tExport Device Info')
        print('4)\tDisable, De-provision, or Re-Enable a Device')
        print('0)\tBack')
        print('\n')

        selection = input('Please Choose an Option: ')
        if selection == '1':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '"'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            cr_id = input('Please enter the Chrome Device Serial Number: ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            time.sleep(1)
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            act = input('What do you want to update?  [location | asset id] ')
            if act == 'location' or act == 'Location' or act == 'loc' or act == 'Loc' or act == 'L' or act == 'l':
                loc = input('Enter new location: ')
                cmd2 = '~/bin/gam/gam update cros ' + id2 + ' location "' + loc + '"'
                os.system(cmd2)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                f.close()
                os.system('rm -rf id.txt')
                break
            elif act == 'asset' or act == 'asset id' or act == 'assetid' or act == 'Asset' or act == 'Asset Id' or \
                    act == 'Asset ID' or act == 'Asset id' or act == 'A' or act == 'a':
                asset = input('Enter new Asset ID: ')
                cmd2 = '~/bin/gam/gam update cros ' + id2 + ' assetid "' + asset + '"'
                os.system(cmd2)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                f.close()
                os.system('rm -rf id.txt')
                break
            else:
                print("Unknown Option Selected!")
                time.sleep(1)
                f.close()
                os.system('rm -rf id.txt')
                input("Press ENTER to Continue...")
                break
        elif selection == '3':
            devices3()
        elif selection == '4':
            devices4()
        elif selection == '0':
            main_menu()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def classroom1():
    while True:
        print('Course Management Menu:')
        print('\n')
        print('1)\tCreate Course')
        print('2)\tUpdate Course')
        print('3)\tGet Course Info')
        print('4)\tDelete Course')
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            al = input('What is the course alias? (All lower lase, no spaces)')
            name = input('What is the course name? ')
            sec = input('What is the course section? (Numbers only)')
            head = input('What is the heading? ')
            room = input('What room is the class in? (No spaces')
            teach = input("What is the teacher's username? ")
            cmd = '~/bin/gam/gam create course alias ' + al + ' name "' + name + '" section ' + sec + ' heading "' \
                  + head + '" room ' + room + ' teacher ' + teach + ' status ACTIVE'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            classroom1_2()
        elif selection == '3':
            al = input('What is the course ID or alias? ')
            cmd = '~/bin/gam/gam info course ' + al
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '4':
            al = input('What is the course ID or alias? ')
            yn = input('Are you sure? This action cannot be undone! [y/N] ')
            if yn == 'y' or yn == 'yes' or yn == 'Y' or yn == 'Yes':
                cmd = '~/bin/gam/gam delete course ' + al
                os.system(cmd)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                break
            elif yn == '' or yn == 'n' or yn == 'no' or yn == 'N' or yn == 'No':
                break
            else:
                print("Unknown Option Selected!")
                time.sleep(1)
                break
        elif selection == '0':
            classroom()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def classroom1_2():  # Classroom main menu option 1, submenu 2
    al = input('What is the course ID or alias that will be updated? ')
    while True:
        print('Update What? ')
        print('\n')
        print('1)\tName')
        print('2)\tSection')
        print('3)\tHeading')
        print('4)\tRoom')
        print('5)\tStatus')
        print('6)\tTeacher')
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            name = input('Enter the new name: ')
            cmd = '~/bin/gam/gam update course ' + al + ' name ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            name = input('Enter new section: ')
            cmd = '~/bin/gam/gam update course ' + al + ' section ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            name = input('Enter new heading: ')
            cmd = '~/bin/gam/gam update course ' + al + ' heading "' + name + '"'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '4':
            name = input('Enter new room: ')
            cmd = '~/bin/gam/gam update course ' + al + ' room ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '5':
            name = input('Enter new status (Must be uppercase): [ACTIVE | ARCHIVED | DECLINED] ')
            cmd = '~/bin/gam/gam update course ' + al + ' status ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '6':
            name = input('Enter new teacher username: ')
            cmd = '~/bin/gam/gam update course ' + al + ' owner ' + name
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            classroom1()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def classroom3():  # Classroom main menu option 3 submenu
    while True:
        print('Guardian Management Menu:')
        print('\n')
        print('1)\tInvite Guardian')
        print('2)\tDelete Guardian')
        print("3)\tView a Student's Guardian(s)")
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            stu = input("What is the student's username? ")
            guard = input("What is the guardian's email address? ")
            cmd = '~/bin/gam/gam create guardianinvite ' + guard + ' ' + stu + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            stu = input("What is the student's username? ")
            guard = input("What is the guardian's email address? ")
            cmd = '~/bin/gam/gam delete guardian ' + guard + ' ' + stu + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            stu = input("What is the student's username? ")
            cmd = '~/bin/gam/gam print guardians student ' + stu + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            classroom()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def classroom4():  # Classroom main menu option 4 submenu
    while True:
        print('Classroom Reports Menu:')
        print('\n')
        print("1)\tView a Teacher's Courses")
        print("2)\tView a Student's Courses")
        print("3)\tView a Course's Participants")
        print('0)\tBack')
        print('\n')

        selection = input("Please Choose an Option: ")
        if selection == '1':
            user = input("What is the teacher's username? ")
            cmd = '~/bin/gam/gam print courses teacher ' + user + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            user = input("What is the student's username? ")
            cmd = '~/bin/gam/gam print courses student ' + user + '@madisonrams.net'
            os.system(cmd)
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            al = input('What is the course ID or alias? ')
            file = input('Output to a CSV file? [Y/n]')
            if file == '' or file == 'y' or file == 'Y' or file == 'yes' or file == 'Yes':
                cmd = '~/bin/gam/gam print course-participants course ' + al + ' > ' + al + '-participants.csv'
                os.system(cmd)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                break
            elif file == 'n' or file == 'N' or file == 'no' or file == 'No':
                cmd = '~/bin/gam/gam print course-participants course ' + al
                os.system(cmd)
                time.sleep(2)
                print('\n')
                input("Press ENTER to Continue...")
                break
            else:
                print("Unknown Option Selected!")
                print('\n')
                time.sleep(2)
                input("Press ENTER to Continue...")
        elif selection == '0':
            classroom()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def devices3():  # Devices main menu option 3 submenu
    while True:
        print('\n')
        print('Chrome Device Info Menu:')
        print('\n')
        print('1)\tView Single Device Info')
        print('2)\tExport All Devices in an OU')
        print('3)\tExport All Devices')
        print('0)\tBack')
        print('\n')

        selection = input('Please Choose an Option: ')
        if selection == '1':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam info cros ' + id2 + ' full'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            os.system('rm -rf id.txt')
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            ou = input('Please enter the full path of the OU you wish to export (Case Sensitive): ')
            ou2 = ou.split("/")[-1]
            cmd = '~/bin/gam/gam print cros full limit_to_ou "' + ou + '" > "' + ou2 + '"-export.csv'
            os.system(cmd)
            time.sleep(1)
            print('Exported as ' + ou2 + '-export.csv')
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            cmd = '~/bin/gam/gam print cros full > all-devices.csv'
            os.system(cmd)
            time.sleep(1)
            print('Device list exported as all-devices.csv')
            time.sleep(2)
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            devices()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def devices4():  # Devices main menu option 4 submenu
    while True:
        print('\n')
        print('Disable/De-Provision/Re-Enable Menu:')
        print('\n')
        print('1)\tDisable')
        print('2)\tRe-Enable')
        print('3)\tDe-Provision')
        print('0)\tBack')
        print('\n')

        selection = input('Please Choose an Option: ')
        if selection == '1':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam update cros ' + id2 + ' action disable acknowledge_device_touch_requirement'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            os.system('rm -rf id.txt')
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam update cros ' + id2 + ' action reenable acknowledge_device_touch_requirement'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            os.system('rm -rf id.txt')
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            devices4_3()
        elif selection == '0':
            devices()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


def devices4_3():  # Devices Main menu option 4. submenu 3
    while True:
        print('\n')
        print('De-Provision Menu:')
        print('\n')
        print('1)\tDe-Provision to Replace With Same Model')
        print('2)\tDe-Provision to Replace With Different Model')
        print('3)\tDe-Provision to Retire')
        print('0)\tBack')
        print('\n')

        selection = input('Please Choose an Option: ')
        if selection == '1':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam update cros ' + id2 + \
                   ' action deprovision_same_model_replace acknowledge_device_touch_requirement'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            os.system('rm -rf id.txt')
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '2':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam update cros ' + id2 + \
                   ' action deprovision_different_model_replace acknowledge_device_touch_requirement'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '3':
            cr_id = input('Please enter the Chrome Device Serial Number (Case sensitive): ')
            cmd = '~/bin/gam/gam print cros query "id:' + cr_id + '" > id.txt'
            print('Looking up the device ID...')
            os.system(cmd)
            time.sleep(1)
            f = open('id.txt')
            id2 = f.readlines()[-1]
            cmd2 = '~/bin/gam/gam update cros ' + id2 + \
                   ' action deprovision_retiring_device acknowledge_device_touch_requirement'
            os.system(cmd2)
            time.sleep(2)
            f.close()
            os.system('rm -rf id.txt')
            print('\n')
            input("Press ENTER to Continue...")
            break
        elif selection == '0':
            devices4()
        else:
            print("Unknown Option Selected!")
            print('\n')
            time.sleep(2)
            input("Press ENTER to Continue...")


cred()
main_menu()
