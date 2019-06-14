import atom
import threading
import signal

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

def main():
	print("Intialization success.")
	print()

	signal.signal(signal.SIGINT, atom.command.sigint_handler)

	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("Привет, Мир.")
	atom.send_notify("Система загружена и готова к работе.")

	while(1):
		pass
	#atom.telegram.telegram.updater.idle()
	
if __name__ == '__main__':
	main()
