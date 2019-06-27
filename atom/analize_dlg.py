import atom.dialog
import atom.utils

class AnalizeDialog(atom.dialog.Dialog):
	def listen(self, text, responce=True):
		words = text.lower().split()
		if words[0] == "анализ:":
			return str(atom.utils.morph_analize(words[1])), 1.0

		return "", 0.0

atom.conver.conversation.add_dialog(AnalizeDialog())