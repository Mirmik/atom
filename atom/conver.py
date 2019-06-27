import atom.dialog

print("Conversation module loaded")

class Conversation(atom.dialog.Dialog):
	def __init__(self):
		self.dialogs = []

	def add_dialog(self, d):
		self.dialogs.append(d)

	def __getitem__(self, idx):
		return self.dialogs[idx]

	def __len__(self):
		return len(self.dialogs)

	def listen(self, text, response=True):
		if len(self.dialogs) == 0:
			return "", 0.0

		responses = []
		for d in self.dialogs:
			#print(d.__class__)
			r = d.listen(text, response) 
			if r is None or len(r) != 2:
				print("Warn: dialog {} return is not valid".format(d.__class__))
			responses.append(r)

		return max(responses, key=lambda x: x[1])

	#def parse(self, text):
	#	return []

	#def interpret(self, sents, **kwargs):
	#	return sents, 0.0, kwargs

	#def respond(self, sents, confidence, **kwargs):
	#	return None

conversation = Conversation()