import pymorphy2
import os

morph = pymorphy2.MorphAnalyzer()

def morph_analize(arg):
	return morph.parse(arg)

def active_base():
	os.system("/home/mirmik/wakonpc.sh")