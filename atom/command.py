print("Command processor initializing.")

import re
import atom.notify
import subprocess
import platform
import signal
import os
import datetime
import traceback
from random import randint

PID = os.getpid()
START_STAMP = datetime.datetime.now()  

def sigint_handler(signum, frame):
	print("sigint_handler")
	sig_names = {23:"NSIG", 22:"SIGABRT", 21:"SIGBREAK", 8:"SIGFPE", 4:"SIGILL",
             2:"SIGINT", 11:"SIGSEGV", 15:"SIGTERM", 0:"SIG_DFL", 1:"SIG_IGN"}

	atom.send_notify("Получил сигнал {}. Завершаюсь.".format(sig_names[signum]))
	os.kill(PID, signal.SIGKILL)

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

def notify_fortune():
	pr = subprocess.Popen(["fortune"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	atom.send_notify(pr.stdout.read().decode("utf-8"))

def get_status():
	status = "Ничего интересного не происходит."
	uptime = str(datetime.datetime.now() - START_STAMP)  #"Я заблудился во времени."
	cputerm = get_temp() #"Я научусь определять её."
	atom.send_notify("""{status}.
Время работы: {uptime}
Имя хостмашины: {hostname}
Температура центрального процессора: {cputerm}"""
		.format(
		uptime=uptime,
		status=status,
		hostname=platform.node(),
		cputerm=cputerm))

kagamine_avas_dir = os.path.join(os.path.dirname(__file__),"img")
kagamine_avas = [os.path.join(kagamine_avas_dir,l) for l in os.listdir(kagamine_avas_dir)]

def send_kagamine_photo():
	atom.telegram.telegram.send_photo(kagamine_avas[randint(0, len(kagamine_avas) - 1)])

def are_you_here():
	atom.telegram.telegram.send_photo(os.path.join(kagamine_avas_dir, "kagamine.jpg"))
	atom.send_notify("Всегда к вашим услугам.")

commands = {
	"анекдот" : notify_fortune,
	"ты здесь?" : are_you_here,
	"усни" : lambda: os.kill(PID, signal.SIGINT),
	"как дела?" : get_status,
	"пасхалка" : send_kagamine_photo
}

def incom(text):
	try:	
		print("incom: {}".format(text.lower()))
		if text.lower() in commands:
			commands[text.lower()]()
			return

		atom.send_notify("Нераспознанная входная последовательность")
	except Exception as ex:
		atom.send_notify("exception in incom thread: {}".format(str(ex)))
		traceback.print_exc()

