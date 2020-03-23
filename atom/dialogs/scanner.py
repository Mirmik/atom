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

	def __str__(self):
		return str(self.pbool)

IPS = {  }

def serve(milliseconds):
	global lastscan_time
	global lastscan_ips

	if milliseconds - lastscan_time > 20000:
		deltatime = milliseconds - lastscan_time
		lastscan_time = milliseconds

		ips = atom.utils.scan_network_doit()
		ips_set = { p[0] for p in ips }

		for p in ips_set:
			if p not in IPS:
				IPS[p] = ip_status(p)

		for p in IPS:
			if p in ips_set:
				IPS[p].pbool.serve(True, deltatime)
			else:
				IPS[p].pbool.serve(False, deltatime)
			
		lastscan_ips = ips

class ScannerDialog(atom.dialog.Dialog):
	def interpret(self, sents, text, **kwargs):
		if text == "статус сети":
			return self.status_notify, 1.0

		return "", 0.0

	def status_notify(self):
		for k in IPS:
			atom.send_notify(k, str(IPS[k]))			
			

atom.conver.conversation.add_dialog(ScannerDialog())


















