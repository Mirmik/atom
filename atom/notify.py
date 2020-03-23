print("Notify module initializing.")

notifiers = []

class notifier:
	def __init__(self):
		pass

	def notify(self, text):
		raise NotImplementedError

def send_notify(*args):
	for n in notifiers:

		#if len(args) == 1:
		#	if isinstance(obj, (list, tuple)):
		#		for o in obj:
		#			n.notify(o)
		#	else:
		#		n.notify(obj)
	
		if len(args) == 1:
			n.notify(args[0])	
		else:
			n.notify(str(args))	