import pymorphy2
import os
from atom.notify import send_notify

morph = pymorphy2.MorphAnalyzer()

def system(cmd):
	pr = subprocess.Popen(cmd.split(),
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	return pr.stdout.read().decode("utf-8")

def morph_analize(arg):
	return morph.parse(arg)

def active_base():
	os.system("/home/mirmik/wakonpc.sh")

def scan_network():
	print("scan_network")

	send_notify(system("nmap -sP 192.168.1.1-255"))