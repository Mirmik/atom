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

		if (len(ips) != len(lastscan_ips)):
			atom.send_notify("Количество айпи в сети изменилось")

			for p in ips:
				if p not in lastscan_ips:
					atom.send_notify(f"Добавилась пара {p}")

			for p in lastscan_ips:
				if p not in ips:
					atom.send_notify(f"Исчезла пара {p}")

		lastscan_ips = ips

