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

def reboot_base():
	return "Процедура перезагрузки базы еще не поддерживается."

def reboot_self():
	system("shutdown -r 1")
	return "Начата процедура перезагрузки."

def scan_network_doit():
	resp = system("nmap -sP 192.168.1.1/24 -oG - | grep Host")
	lines = resp.split("\n")
	return [(l.split()[1], l.split()[2]) for l in lines if l!=""]


def scan_network_impl():
	ips = scan_network_doit()

	send_notify("В сети существуют адреса:")
	for i in ips:
		send_notify("{} {}".format(*i))


def scan_network():
	thr = threading.Thread(target=scan_network_impl)
	thr.start()
	return "Начинаю сканирование сети."
