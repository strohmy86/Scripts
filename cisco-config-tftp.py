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

name = 'cisco-config-tftp'
import easysnmp
import sys
import time
import random
import socket
import tftpy
import threading
import ctypes, os

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
    
class Msgs:  # Various repeated messages
    cont = 'Press ENTER to Continue...'
    err = 'Invalid Option Selected!'
    choose = 'Please Choose an Option:'  

def cred():

    print('\n')
    print(Color.DARKCYAN)
    print("*********************************")
    print("*  Python 3 Script For Copying  *")
    print("* Cisco Configs To/From A TFTP  *")
    print("* Server VIA the SNMP Protocol  *")
    print("*                               *")
    print("*   Written and maintained by   *")
    print("*          Luke Strohm          *")
    print("*     strohm.luke@gmail.com     *")
    print("*  https://github.com/strohmy86 *")
    print("*                               *")
    print("*********************************")
    print(Color.END)
 
def admin_check():
	try:
		is_admin = os.getuid() == 0
	except AttributeError:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

	if is_admin == True:
		main_menu()
	else:
		print(Color.RED+Color.BOLD+'This program requires Admin privileges. Please rerun as an administrator.'+ Color.END)
		sys.exit()
	
 
def main_menu():  # Main Menu
    while True:
        print('\n')
        print(Color.PURPLE + 'Main Menu:' + Color.END)
        print('\n')
        print('1)   Copy Config FROM Cisco Device TO a TFTP Server')
        print('2)   Copy Config TO Cisco Device FROM a TFTP Server')
        print('0)   Exit')
        print('\n')

        selection1 = input(Color.BOLD + Msgs.choose + Color.END)
        if selection1 == '0':
            sys.exit()
        elif selection1 == '1':
            toTftp()
        elif selection1 == '2':
            frTftp()
        else:
            print(Color.RED + Msgs.err + Color.END)
            print('\n')
            time.sleep(2)
            input(Color.GREEN + Msgs.cont + Color.END)       

def toTftp():
	# OID List
	# Protocol = .1.3.6.1.4.1.9.9.96.1.1.1.1.2.<Random Number> i 1
	# Src File Type = .1.3.6.1.4.1.9.9.96.1.1.1.1.3.<Random Number> i 4
	# Dest File Type = .1.3.6.1.4.1.9.9.96.1.1.1.1.4.<Random Number> i 1
	# Srv Address = .1.3.6.1.4.1.9.9.96.1.1.1.1.5.<Random Number> a <IP Address>
	# Dest File Name = .1.3.6.1.4.1.9.9.96.1.1.1.1.6.<Random Number> s <File Name>
	# Entry Row Stats = .1.3.6.1.4.1.9.9.96.1.1.1.1.14.<Random Number> i 4
	
	rand = str(random.randint(100,999))
	swAddr = input('What is the IP address of the switch?   ')
	comm = input('What is the SNMP Community?   ')
	print(Color.YELLOW+'What is the IP address of the TFTP server?')
	print('Leave blank to use the built-in TFTP server. '+Color.END)
	tftpAddr = str(input('IP address:   ') or '127.0.0.1')
	fileName = input('Enter the filename (Optional: w/Path ):   ')
	nameOnly = fileName.split('/')[-1]
	
	if tftpAddr != '127.0.0.1':
		tup = [
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.2.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.3.'+rand, '4', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.4.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.5.'+rand, tftpAddr, 'a'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.6.'+rand, fileName, 's'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.14.'+rand, '4', 'i')
			]

		session = easysnmp.Session(hostname=swAddr, community=comm, version=2)
		session.set_multiple(tup)
		time.sleep(2)
		input(Color.GREEN + Msgs.cont + Color.END)
		main_menu()	
	else:
		print('Starting TFTP Server....')
		server = tftpy.TftpServer(os.getcwd())
		server_thread = threading.Thread(target=server.listen, kwargs={'listenip': '0.0.0.0', 'listenport': 69})
		server_thread.start()
		time.sleep(2)
		print('TFTP Server started in current working directory.')
		ipAddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
		if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
		s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
		socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
		
		tup = [
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.2.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.3.'+rand, '4', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.4.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.5.'+rand, ipAddr, 'a'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.6.'+rand, nameOnly, 's'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.14.'+rand, '4', 'i')
			]

		session = easysnmp.Session(hostname=swAddr, community=comm, version=2)
		session.set_multiple(tup)
		time.sleep(2)
		success = os.path.isfile(os.getcwd()+'/'+nameOnly)
		if success == True:
			print(Color.GREEN+'Success!'+Color.END)
			server.stop(now=False)
			server_thread.join()
			input(Color.GREEN + Msgs.cont + Color.END)
			main_menu()
		else:
			print(Color.RED+'I failed to download the config.'+Color.END)
			server.stop(now=False)
			server_thread.join()
			yn = input('Would you like to try again? [Y/n]  ')
			if yn == 'Y' or yn == 'yes' or yn == '':
				toTftp()
			else:
				main_menu()
				
def frTftp():
	# OID List
	# Protocol = .1.3.6.1.4.1.9.9.96.1.1.1.1.2.<Random Number> i 1
	# Src File Type = .1.3.6.1.4.1.9.9.96.1.1.1.1.3.<Random Number> i 1
	# Dest File Type = .1.3.6.1.4.1.9.9.96.1.1.1.1.4.<Random Number> i 4
	# Srv Address = .1.3.6.1.4.1.9.9.96.1.1.1.1.5.<Random Number> a <IP Address>
	# Dest File Name = .1.3.6.1.4.1.9.9.96.1.1.1.1.6.<Random Number> s <File Name>
	# Entry Row Stats = .1.3.6.1.4.1.9.9.96.1.1.1.1.14.<Random Number> i 4
	
	rand = str(random.randint(100,999))
	swAddr = input('What is the IP address of the switch?   ')
	comm = input('What is the SNMP Community?   ')
	print(Color.YELLOW+'What is the IP address of the TFTP server?')
	print('Leave blank to use the built-in TFTP server and a local file. '+Color.END)
	tftpAddr = str(input('IP address:   ') or '127.0.0.1')
	if tftpAddr == '127.0.0.1':
		print(Color.YELLOW+'The default file path is the current working directory.')
		print('Your file MUST be inside or below this directory'+Color.END)
		
	fileName = input('Enter the filename (w/path if below default directory):   ')
	
	if tftpAddr != '127.0.0.1':
		tup = [
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.2.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.3.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.4.'+rand, '4', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.5.'+rand, tftpAddr, 'a'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.6.'+rand, fileName, 's'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.14.'+rand, '4', 'i')
			]

		session = easysnmp.Session(hostname=swAddr, community=comm, version=2)
		session.set_multiple(tup)
		time.sleep(2)
		input(Color.GREEN + Msgs.cont + Color.END)
		main_menu()	
	else:
		print('Starting TFTP Server....')
		server = tftpy.TftpServer(os.getcwd())
		server_thread = threading.Thread(target=server.listen, kwargs={'listenip': '0.0.0.0', 'listenport': 69})
		server_thread.start()
		time.sleep(2)
		print('TFTP Server started in current working directory.')
		ipAddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
		if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
		s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
		socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
		
		tup = [
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.2.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.3.'+rand, '1', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.4.'+rand, '4', 'i'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.5.'+rand, ipAddr, 'a'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.6.'+rand, fileName, 's'),
			('.1.3.6.1.4.1.9.9.96.1.1.1.1.14.'+rand, '4', 'i')
			]

		session = easysnmp.Session(hostname=swAddr, community=comm, version=2)
		session.set_multiple(tup)
		time.sleep(10)
		server.stop(now=False)
		server_thread.join()
		input(Color.GREEN + Msgs.cont + Color.END)
		main_menu()	
	
cred()
admin_check()