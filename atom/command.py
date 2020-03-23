print("Command processor initializing.")

#import spacy
#import ru2

import re
import atom.notify
import signal
import os
import traceback
from random import randint

import atom.conver

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

PID = os.getpid()

def sigint_handler(signum, frame):
	print("sigint_handler")
	sig_names = {23:"NSIG", 22:"SIGABRT", 21:"SIGBREAK", 8:"SIGFPE", 4:"SIGILL",
			 2:"SIGINT", 11:"SIGSEGV", 15:"SIGTERM", 0:"SIG_DFL", 1:"SIG_IGN"}

	atom.send_notify("Получил сигнал {}. Завершаюсь.".format(sig_names[signum]))
	os.kill(PID, signal.SIGKILL)

def incom(text):
	if len(text) == 0:
		return

	try:	
		text = text.strip().lower()
		print("incom: {}".format(text))

		result, confidence = atom.conversation.listen(text)
		
		if confidence > 0.0:
			if callable(result):
				result()

			else:
				atom.send_notify(result)
		else:		
			atom.send_notify("Нераспознанная входная последовательность")
			
			for t in text.split():
				atom.send_notify(str(morph.parse(t)))

			
	
	except Exception as ex:
		atom.send_notify("exception in incom thread: {}".format(str(ex)))
		traceback.print_exc()

