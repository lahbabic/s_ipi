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
	
def gateway_ip():
	gws = netifaces.gateways()
	gateway_ip = gws['default'][netifaces.AF_INET][0]
	iface = gws['default'][netifaces.AF_INET][1]
	return gateway_ip , iface

if __name__ == "__main__":
	f = "/etc/network/interfaces"
	check_for_root()
	if not check_file_writeable(f):
		sys.exit("")
	save_file(f)
	gw_ip , iface = gateway_ip()