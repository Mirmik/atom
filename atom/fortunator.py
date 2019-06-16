import atom.dialog
import atom.conver
import os
import subprocess
from random import randint

import atom.fixcommand

from atom.spacymodel import nlp, get_first_verb, get_first_noun

print("Fortunator was loaded")

verbs_print = set(["скажи", "сказать", "расскажи", "рассказать", "напиши", "писать"])
verbs_send = set(["отправить"])
status_noun = set(["статус", "состояние"])
fortune_noun = set(["фортунка", "анекдот"])
pict_noun = set(["фотография", "картинка", "фотка", "изображение"])

kagamine_avas_dir = os.path.join(os.path.dirname(__file__),"img")
kagamine_avas = [os.path.join(kagamine_avas_dir,l) for l in os.listdir(kagamine_avas_dir)]

def get_random_picture():
	return atom.wrapers.image(kagamine_avas[randint(0, len(kagamine_avas) - 1)]), 1.0

def system_fortune():
	pr = subprocess.Popen(["fortune"],
						  stdin=subprocess.PIPE,
						  stdout=subprocess.PIPE)
	return pr.stdout.read().decode("utf-8")

class Fortunator(atom.dialog.Dialog):
	def parse(self, text):
		doc = nlp(text)
		return doc.sents

	def print_action(self, l0):
		noun = get_first_noun(l0)

		if noun.lemma_ in fortune_noun:
			return system_fortune(), 1.0
		if noun.lemma_ in status_noun:
			return atom.fixcommand.get_status()
		else:
			return "", 0.0


	def send_action(self, l0):
		noun = get_first_noun(l0)

		if noun.lemma_ in pict_noun:
			return get_random_picture(), 1.0
		else:
			return "", 0.0

	def interpret(self, sents, **kwargs):
		sarr = []
		for s in sents:
			sarr.append(s)

		l0 = sarr[0]

		for l in l0:
			atom.spacymodel.print_token(l)

		verb = get_first_verb(l0)

		if verb is None:
			return "", 0.0

		if verb.lemma_ in verbs_print:
			return self.print_action(l0)

		if verb.lemma_ in verbs_send:
			return self.send_action(l0)

		return "", 0.0

atom.conver.conversation.add_dialog(Fortunator())