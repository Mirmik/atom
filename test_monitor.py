#!/usr/bin/env python3
import pycrow
import json

#pycrow.diagnostic_setup(True, True)
pycrow.create_udpgate(12, 10042)

class AliveRecord:
	def __init__(self, name, timestamp):

alive_list = {}

def incom(pack):
	print("incoming", pack.message())

	try:
		data = json.loads(pack.message())
	except:
		return

	


def undel(pack):
	print("undeliver")

node = pycrow.PyNode(incom, undel)
node.bind(42)

pycrow.start_spin()
pycrow.join_spin()