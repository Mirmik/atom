import atom.notify
import atom.utils

lastscan_time = 0
lastscan_ips = []

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - self.lastscan > 30000:
		self.lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()
		atom.send_notify(ips)

		if (len(ips) != len(self.lastscan_ips)):
			atom.send_notify("Количество айпи в сети изменилось")

		self.lastscan_ips = ips

