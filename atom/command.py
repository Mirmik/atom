print("Command processor initializing.")

import re
import atom.notify
import subprocess
import platform
import signal
import os
import datetime

PID = os.getpid()
START_STAMP = datetime.datetime.now()  

def sigint_handler(signum, frame):
	sig_names = {23:"NSIG", 22:"SIGABRT", 21:"SIGBREAK", 8:"SIGFPE", 4:"SIGILL",
             2:"SIGINT", 11:"SIGSEGV", 15:"SIGTERM", 0:"SIG_DFL", 1:"SIG_IGN"}

	atom.send_notify("Получил сигнал {}. Завершаюсь.".format(sig_names[signum]))

#signal.signal(signal.SIGINT, sigint_handler)

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

commands = {
	"анекдот" : notify_fortune,
	"ты здесь?" : lambda: atom.send_notify("Всегда к вашим услугам."),
	"усни" : lambda: os.kill(PID, signal.SIGINT),
	"как дела?" : lambda: get_status()
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
