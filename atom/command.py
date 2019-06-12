print("Command processor initializing.")

import atom.notify
import subprocess
import signal
import os

PID = os.getpid()

def notify_fortune():
	pr = subprocess.Popen(["fortune"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	atom.send_notify(pr.stdout.read().decode("utf-8"))

commands = {
	"анекдот" : notify_fortune,
	"ты здесь?" : lambda: atom.send_notify("Всегда к вашим услугам."),
	"усни" : lambda: os.kill(PID, signal.SIGINT)
}

def incom(text):
	print("incom: {}".format(text.lower()))
	if text.lower() in commands:
		commands[text.lower()]()
		return

	atom.send_notify("Нераспознанная входная последовательность")