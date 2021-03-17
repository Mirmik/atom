#!/usr/bin/env python3
import pycrow
import json
import time
import atom
import threading

pycrow.create_udpgate(12, 10042)

class AliveRecord:
	def __init__(self, name):
		self.name = name
		self.timestamp = time.time()
		self.state = False

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
		alive_list[name] = AliveRecord(name)

	alive_list[name].update(time.time())


def undel(pack):
	pass

def func_checker():
	while 1:
		time.sleep(3)
		for k,v in alive_list.items():
			v.check()

node = pycrow.PyNode(incom, undel)
node.bind(42)

thr = threading.Thread(target=func_checker, args=())
thr.start()

pycrow.start_spin()
