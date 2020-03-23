#!/usr/bin/env python3

import atom
import argparse
import threading
import signal

import datetime
import time
import io
import sys
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

import threading
#import atom.scanner

import atom.dialogs.scanner

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def imitate():
	atom.incom("отправь картинку")

def self_loop():
	today_greatings = False

	while 1:
		try:
			milliseconds = int(round(time.time() * 1000))

			now = datetime.datetime.now()
			hour = now.hour
			minu = now.minute

			atom.dialogs.scanner.serve(milliseconds)

			if hour == 8 and 20 < minu < 40:
				if today_greatings is False:
					today_greatings = True
					atom.send_notify("Доброе утро")

			if hour == 0:
				today_greatings = False

			time.sleep(1)

		except Exception as ex:
			print(ex)

def console_reader():
	while 1:
		atom.incom(input())

def main():
	print("Intialization success.")
	print()

	parser = argparse.ArgumentParser()
	parser.add_argument("--telegramm", action="store_true")
	parser.add_argument("--console", action="store_true")
	args = parser.parse_args()

	if args.telegramm:
		from atom._telegram import enable_telegramm_notifier
		enable_telegramm_notifier()

	if args.console:
		console_thr = threading.Thread(target=console_reader)
		console_thr.start()		

	signal.signal(signal.SIGINT, atom.command.sigint_handler)

	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("utf-8 test: 黒い猫の星は撤回しない")
	atom.send_notify("Привет, Мир.")
	atom.send_notify("Система загружена и готова к работе.")

	sloop = threading.Thread(target = self_loop, args=())
	sloop.start()

	while(1):
		time.sleep(0.5)

if __name__ == '__main__':
	main()
