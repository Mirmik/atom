print("Notify module initializing.")

notifiers = []

class notifier:
	def __init__(self):
		pass

	def notify(self, text):
		raise NotImplementedError

def send_notify(obj):
	for n in notifiers:

		if isinstance(obj, (list, tuple)):
			for o in obj:
				n.notify(o)
		else:
			n.notify(obj)
		