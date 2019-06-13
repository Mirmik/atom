print("Command processor initializing.")

import re
import atom.notify
import subprocess
import platform
import signal
import os

PID = os.getpid()

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
	uptime = "Я заблудился во времени."
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
