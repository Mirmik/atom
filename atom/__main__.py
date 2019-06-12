import atom
import threading

def main():
	print("Intialization success.")
	print()

	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("*")
	atom.send_notify("Привет, Мир.")
	atom.send_notify("Система загружена и готова к работе.")

	atom.telegram.telegram.updater.idle()
	
if __name__ == '__main__':
	main()