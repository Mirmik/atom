import atom.notify
import atom.utils

lastscan_time = 0
lastscan_ips = []

outed = dict()

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - lastscan_time > 20000:
		lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()

		for p in ips:
			if p not in lastscan_ips and p[0] not in outed:
				atom.send_notify(f"Сканер зарегистрировал новую пару {p}")
			
			if p[0] in outed:
				del outed[p[0]]

		for p in lastscan_ips:
			if p not in ips:
				print("Добавляю в outed", (milliseconds, p))
				outed[p[0]] = (milliseconds, p)
				
		for k, v in outed.items():
			if milliseconds - v[0] > 100000:
				atom.send_notify(f"Сканер зафиксировал исчезновение пары {v[1]}")
				del outed[k]

		lastscan_ips = ips

