import atom.dialog
import atom.conver
import atom.wrapers
import atom.scanner

import signal
from random import randint
import subprocess
import os
import re
import platform
import datetime

PID = os.getpid()
START_STAMP = datetime.datetime.now()  

def get_temp():
	pr = subprocess.Popen(["sensors"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	lines = pr.stdout.readlines()
	for l in lines:
		l = l.decode("utf-8")
		if "Core 0" in l:
			l = re.findall(r'\+[\.0-9]*.C', l)
			return "{} (критическая: {}, максимальная: {})".format(*l)
	return "undefined"

def get_status():
	status = "Ничего интересного не происходит."
	uptime = str(datetime.datetime.now() - START_STAMP)  #"Я заблудился во времени."
	cputerm = get_temp() #"Я научусь определять её."
	return (f"""{status}.
Время работы: {uptime}
Имя хостмашины: {hostname}
Температура центрального процессора: {cputerm}
Количество машин в локальной сети: {len(atom.scanner.lastscan_ips)}""", 1.0)

kagamine_avas_dir = os.path.join(os.path.dirname(__file__),"img")
kagamine_avas = [os.path.join(kagamine_avas_dir,l) for l in os.listdir(kagamine_avas_dir)]

def send_kagamine_photo():
	return atom.wrapers.image(kagamine_avas[randint(0, len(kagamine_avas) - 1)]), 1.0

def are_you_here():
	return (atom.wrapers.image(os.path.join(kagamine_avas_dir, "kagamine.jpg")), "Всегда к вашим услугам."), 1.0

def sleep_please():
	os.kill(PID, signal.SIGINT)
	return "Не забудь вернуть меня.", 1.0

commands = {
	"ты здесь?" : are_you_here,
	"усни" : sleep_please,
	"как дела?" : get_status,
	"пасхалка" : send_kagamine_photo
}

print("Fixcommand was loaded")

class Fixcommand(atom.dialog.Dialog):
	def listen(self, text, responce=True):
		text = text.lower()
		if text in commands:
			return commands[text]()

		return "", 0.0

atom.conver.conversation.add_dialog(Fixcommand())
