import abc

class Dialog:
	def listen(self, text, response=True, **kwargs):
		sents = self.parse(text)
		reply, confidence = self.interpret(sents, **kwargs)
		return reply, confidence

	@abc.abstractmethod
	def parse(self, text):
		return []

	@abc.abstractmethod
	def interpret(self, sents, **kwargs):
		return sents, 0.0, kwargs