import atom.notify
import atom.utils

lastscan_time = 0
lastscan_ips = []

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - lastscan_time > 20000:
		lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()

		for p in ips:
			if p not in lastscan_ips:
				atom.send_notify(f"Сканер зарегистрировал новую пару {p}")

		for p in lastscan_ips:
			if p not in ips:
				atom.send_notify(f"Сканер зафиксировал исчезновение пары {p}")

		lastscan_ips = ips

