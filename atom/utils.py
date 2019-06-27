import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def morph_analize(arg):
	return morph.parse(arg)
