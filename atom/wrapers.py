class image:
	def __init__(self, path):
		self.path = path

	def __repr__(self):
		return "atom.image.wraper: path='{}'".format(self.path)