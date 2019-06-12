import atom.notify

print("Console module initializing.")

class ConsoleNotifier(atom.notify.notifier):
	def __init__(self):
		super().__init__()

	def notify(self, text):
		print("notify: {}".format(text))

atom.notify.notifiers.append( ConsoleNotifier() )

