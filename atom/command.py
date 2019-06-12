print("Command processor initializing.")

import atom.notify
import subprocess

def notify_fortune():
	pr = subprocess.Popen(["fortune"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	atom.send_notify(pr.stdout.read().decode("utf-8"))

commands = {
	"анекдот" : notify_fortune,
	"Ты здесь?" : lambda: atom.send_notify("Всегда к вашим услугам."),
}

def incom(text):
	print("incom: {}".format(text))
	if text in commands:
		commands[text]()
		return

	atom.send_notify("Нераспознанная входная последовательность")