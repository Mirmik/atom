import atom
import threading
import signal

import io
import sys
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def imitate():
	atom.incom("отправь картинку")

def main():
	print("Intialization success.")
	print()

	signal.signal(signal.SIGINT, atom.command.sigint_handler)

	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("utf-8 test: 黒い猫の星は撤回しない")
	atom.send_notify("Привет, Мир.")
	atom.send_notify("Система загружена и готова к работе.")

	#imitate()

	while(1):
		pass

if __name__ == '__main__':
	main()
