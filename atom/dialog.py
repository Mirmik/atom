import pymorphy2
morph = pymorphy2.MorphAnalyzer()

class Dialog:
	def __init__(self):
		self.morph = morph

	def listen(self, text, response=True, **kwargs):
		sents = self.parse(text)
		reply, confidence = self.interpret(sents, text, **kwargs)
		return reply, confidence

	def parse(self, text):
		parr = []

		for t in text.split():
			parr.append(morph.parse(t))

		return parr

	def interpret(self, sents, text, **kwargs):
		return sents, 0.0, kwargs