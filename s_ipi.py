#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from __future__ import print_function
from subprocess import Popen, PIPE
import os, sys
try:
	import netifaces
except ImportError:
	install_binary("python3-netifaces")

W = '\033[1;37m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray

def print_done():
    print(W+"["+G+"Done"+W+"]")
    
def print_ok():
    print(W+"["+G+"OK"+W+"]")
    
def print_err():
    print(W+"["+R+"error"+W+"]")
    
def check_for_root():
	print('cheking for root...',end="")
	if not os.geteuid() == 0:
	    sys.exit('Script must be run as root')
	print_ok()

def check_file_writeable(file_path=""):
	name = file_path.split('/')[-1]
	print('cheking if '+B+name+W+' exist...',end="")
	if not os.path.isfile(file_path):
		print_err()
		sys.exit("")
	print_ok()
	try:
		print("cheking if "+B+name+W+" is writeable...",end="")
		file = open(file_path, "w")
		file.close()
		print_ok()
		return True
	except:
		print_err()
		return False

def check_for_binarys(binarys_array=[]):
	paths = os.environ["PATH"].split(':') 
	print(paths)
	for needed_binary in binarys_array:
		for path in paths:
			if os.path.isfile(path+'/'+needed_binary[0]):
				needed_binary[1] = True

	for needed_binary in binarys_array:
		print('cheking for '+needed_binary[0]+"...",end="")
		if not needed_binary[1]:
			print(W+"["+B+"NOT FOUND"+W+"]")
			binary = str(needed_binary[0])
			install_binary(binary)
		else:
			print_ok()
	
def install_binary(b=""):
	if input("Do you want to install it? [y/n] ") == 'y':
		if not os.system('apt-get install '+b)==0:
			sys.exit('Can\'t install '+b)
	else:
		sys.exit('Please install needed binarys to run this script')

def save_file(file_path=""):
	name = file_path.split('/')[-1]
	print("Saving  "+B+name+W+"...",end="")
	cmd = (["cp",file_path,file_path+".sav"])
	with Popen(cmd, stdout=PIPE ,stderr=PIPE) as proc:
		if not (proc.stderr.read().decode('utf-8') == ""):
			print_err()
			sys.exit("")
		print_done()
	
def check_for_up_ifaces():
	print('checking for up interfaces...',end="")
	try:
		ifaces = netifaces.interfaces()
		print_ok()
		if (ifaces[0] == 'lo') or (ifaces[0] == 'lo0'):
			ifaces.pop(0)
		adresses = netifaces.ifaddresses(ifaces[0]) 
		print(ifaces)
	except NameError:
		print_err()
		sys.exit("")



if __name__ == "__main__":
	f = "/etc/network/interfaces"
	#needed_binarys = [['python3-netifaces',False]]
	check_for_root()
	#check_for_binarys(needed_binarys)
	if not check_file_writeable(f):
		sys.exit("")
	save_file(f)
	check_for_up_ifaces()