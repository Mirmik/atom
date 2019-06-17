import atom.dialog
import atom.utils
import atom.modes

def debug_mode_setter(args):
	on = int(args[1])
	if on:
		atom.modes.debug_mode = True
		return "on"
	else:
		atom.modes.debug_mode = False
		return "off"		

commands = {
	"debug": debug_mode_setter
}

class CommandDialog(atom.dialog.Dialog):
	def listen(self, text, responce=True):
		words = text.lower().split()
		if words[0][0] == '$':
			if words[0][1:] in commands:
				ret = commands[words[0][1:]](words)
				return str(ret), 1.0
			else:
				return "Команда не найдена", 1.0

		return "", 0.0

atom.conver.conversation.add_dialog(CommandDialog())