import atom.notify
import atom.utils

lastscan_time = 0
lastscan_ips = []

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - lastscan_time > 30000:
		lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()
		atom.send_notify(ips)

		if (len(ips) != len(lastscan_ips)):
			atom.send_notify("Количество айпи в сети изменилось")

		lastscan_ips = ips

