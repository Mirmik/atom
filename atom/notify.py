print("Notify module initializing.")

notifiers = []

class notifier:
	def __init__(self):
		pass

	def notify(self, text):
		raise NotImplementedError

def send_notify(text):
	for n in notifiers:
		n.notify(text)
		