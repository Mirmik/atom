import atom.notify
import atom.utils

import atom.probevent

lastscan_time = 0
lastscan_ips = []

outed = dict()

class ip_status:
	def __init__(self, ip):
		self.pbool = atom.probevent.AperiodicBooleanState(
			true_timeconst=None, 
			false_timeconst=180_000, 
			trigger=0.45, 
			initstate=0
		)
		self.pbool.set_on_change_handle(self.on_change)
		self.ip = ip

	def on_change(self, en):
		atom.send_notify(f"on_change: {self.ip} {en}")

IPS = {  }

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - lastscan_time > 20000:
		deltatime = milliseconds - lastscan_time
		lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()
		ips_set = { p[0] for p in ips }

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

		for p in ips_set:
			if p not in IPS:
#				print("create", p)
				IPS[p] = ip_status(p)

		for p in IPS:
			print(p)
			if p in ips_set:
				IPS[p].pbool.serve(True, deltatime)
			else:
				IPS[p].pbool.serve(False, deltatime)
			
		lastscan_ips = ips

