#import spacy
#import os
#
#nlp = spacy.load(os.path.join(os.path.dirname(__file__),'ru2'))
#nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
#
#
#def get_first_verb(tokens):
#	for t in tokens:
#		if t.pos_ == "VERB":
#			return t
#
#
#def get_first_noun(tokens):
#	for t in tokens:
#		if t.pos_ == "NOUN":
#			return t
#
#
#def print_token(token):
#	print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#            token.shape_, token.is_alpha, token.is_stop)