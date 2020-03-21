import pymorphy2
import os
import threading

from atom.notify import send_notify
import subprocess

morph = pymorphy2.MorphAnalyzer()

def system(cmd):
	pr = subprocess.Popen(cmd,
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE, shell=True)
	return pr.stdout.read().decode("utf-8")

def morph_analize(arg):
	return morph.parse(arg)

def active_base():
	os.system("/home/mirmik/wakonpc.sh")


def scan_network_impl():
	resp = system("nmap -sP 192.168.1.1/24 -oG - | grep Host")
	lines = resp.split("\n")
	ips = [l[1] for l in lines]
	send_notify(resp)
	send_notify(ips)

def scan_network():
	thr = threading.Thread(target=scan_network_impl)
	thr.start()
