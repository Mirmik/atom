#!/usr/bin/env python3
import pycrow
import pycrow as crow
import json
import time
import atom
import atom.notify
import threading

NODE = None
pycrow.create_udpgate(12, 10042)

class AliveRecord:
	def __init__(self, name, addr=None):
		self.name = name
		self.timestamp = time.time()
		self.state = False
		self.addr = addr

	def update(self, timestamp):
		if self.state is False:
			self.state = True
			self.notify_enable()

		self.timestamp = time.time()

	def check(self):
		if self.state is False:
			return

		curtime = time.time()
		if curtime - self.timestamp > 10:
			self.state = False
			self.notify_disable()

	def notify_enable(self):
		atom.say(f"Enabled: {self.name}")

	def notify_disable(self):
		atom.say(f"Disabled: {self.name}")


alive_list = {}

def incom(pack):
	try:
		data = json.loads(pack.message())
	except:
		print("warn: unresolved format")
		return

	try:
		name = data["mnemo"]
	except:
		print("warn: unresolved key")
		return

	if name not in alive_list:
		alive_list[name] = AliveRecord(name, addr=pack.addr())

	alive_list[name].update(time.time())

def undel(pack):
	pass

def func_checker():
	while 1:
		time.sleep(3)
		to_del = []
		for k,v in alive_list.items():
			v.check()
			if v.state is False:
				to_del.append(k)
			
			#NODE.send(42, v.addr, "hello", 0, 50, False)

		for k in to_del:
			del alive_list[k]


class MonitorNotifier(atom.notify.notifier):
	def __init__(self):
		super().__init__()

	def notify(self, text):
		for k,v in alive_list.items():
			NODE.send(42, v.addr, text, 0, 50, False)


atom.notify.notifiers.append( MonitorNotifier() )




node = pycrow.PyNode(incom, undel)
node.bind(42)
NODE = node

thr = threading.Thread(target=func_checker, args=())
thr.start()

#pycrow.diagnostic_setup(True, False)
pycrow.start_spin()
