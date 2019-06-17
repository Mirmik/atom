import atom.dialog
import atom.conver
import os
import subprocess
from random import randint

import atom.fixcommand

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

#from atom.spacymodel import nlp, get_first_verb, get_first_noun

print("Fortunator was loaded")

verbs_print = set(["скажи", "сказать", "расскажи", "рассказать", "напиши", "писать"])
verbs_send = set(["отправить", "прислать"])
status_noun = set(["статус", "состояние"])
fortune_noun = set(["фортунка", "анекдот"])
pict_noun = set(["фотография", "картинка", "фотка", "изображение"])

kagamine_avas_dir = os.path.join(os.path.dirname(__file__),"img")
kagamine_avas = [os.path.join(kagamine_avas_dir,l) for l in os.listdir(kagamine_avas_dir)]

def get_random_picture():
	return atom.wrapers.image(kagamine_avas[randint(0, len(kagamine_avas) - 1)])

def system_fortune():
	pr = subprocess.Popen(["fortune"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	return pr.stdout.read().decode("utf-8")

class Fortunator(atom.dialog.Dialog):
	def print_action(self, l0):
		noun = self.get_first_noun(l0)

		if noun.normal_form in fortune_noun:
			return system_fortune(), 1.0
		if noun.normal_form in status_noun:
			return atom.fixcommand.get_status()
		else:
			return "", 0.0


	def send_action(self, l0):
		noun = self.get_first_noun(l0)

		if noun.normal_form in pict_noun:
			return get_random_picture(), 1.0
		else:
			return "", 0.0

	def get_first_verb(self, sents):
		for t in sents:
			if t[0].tag.POS == "VERB":
				return t[0]
		return None

	def get_first_noun(self, sents):
		for t in sents:
			if t[0].tag.POS == "NOUN":
				return t[0]
		return None

	def parse(self, text):
		parr = []

		for t in text.split():
			parr.append(morph.parse(t))

		return parr

	def interpret(self, sents, **kwargs):
		verb = self.get_first_verb(sents)

		if verb is None:
			return "", 0.0

		ret = None

		if atom.modes.debug_mode:
			atom.send_notify("debug_morph: " + str(sents))
			atom.send_notify("first_verb: " + str(self.get_first_noun(sents)))
			atom.send_notify("first_noun: " + str(self.get_first_noun(sents)))

		if verb.normal_form in verbs_print:
			ret = self.print_action(sents)

		if verb.normal_form in verbs_send:
			ret = self.send_action(sents)

		if ret is not None and ret[1] > 0.00001:
			return ret
		else:
			return "", 0.0

atom.conver.conversation.add_dialog(Fortunator())