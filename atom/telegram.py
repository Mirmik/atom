import atom.notify
import atom.command
import telegram
import os

import socket
import socks

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

proxy_ip = '127.0.0.1'  # change your proxy's ip
proxy_port = 9050  # change your proxy's port

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_ip, proxy_port)
#socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, proxy_ip, 9080)
#socket.socket = socks.socksocket


print("Telegram module initializing.")

token_filepath = os.path.expanduser("~/.atomtoken")
chat_filepath = os.path.expanduser("~/.atomchat")

if os.path.exists(chat_filepath):
	chat = int(open(chat_filepath).read())
else:
	chat = None

REQUEST_KWARGS={
	'proxy_url': 'socks5://127.0.0.1:9050',
}

def filterchat(func):
	def decfunc(bot, update):
		if chat is not None:
			if update.message.chat_id != chat:
				return
		return func(bot, update)

	return decfunc

@filterchat
def start(bot, update):	
	try:
		print("start command in:", update.message.chat_id)
		bot.send_message(chat_id=update.message.chat_id, text="Hello, Mir!")
	except Exception as ex:
		print(ex)

@filterchat
def input_message(bot, update):
	try:
		atom.incom(update.message.text)
	except Exception as ex:
		print(ex)


class Telegram(atom.notify.notifier):
	def __init__(self):
		super().__init__()

		try:
			token = open(token_filepath).read()
		except Exception as ex:
			print("Telegram: token loading error")
			print(ex)
			exit(0)

		self.bot = Bot(token=token)
		self.updater = Updater(bot=self.bot, user_sig_handler=atom.command.sigint_handler, request_kwargs = REQUEST_KWARGS)

		try:
			answer = self.bot.get_me()
			print("Telegram bot:", answer)
		except Exception as ex:
			print("Autorize telegram bot fault: \n{}".format(ex))
			exit(0)

		start_handler = CommandHandler('start', start)
		self.updater.dispatcher.add_handler(start_handler)

		input_message_handler = MessageHandler(Filters.text, input_message)
		self.updater.dispatcher.add_handler(input_message_handler)

	def notify(self, text):
		try:
			if chat is not None:
				if isinstance(text, atom.wrapers.image):
					self.send_photo(text.path)
				else:
					self.bot.send_message(chat_id=chat, text=text, **REQUEST_KWARGS)
			else:
				print("Warn: telegram chat isn't defined")
		except Exception as ex:
			print("telegram.send_mesage fault with ex: {}".format(ex))

	def send_photo(self, path):
		print("Отправлено изображение:", path)
		self.bot.send_photo(chat, open(path, 'rb'))

	def start_polling(self):
		print("Telegram polling was started.")
		self.updater.start_polling(clean=True)
	
	def get_updates(self):
		updates = self.bot.get_updates()
		print([u.message.text for u in updates])

telegram = Telegram()
#telegram.get_updates()
telegram.start_polling()
	
atom.notify.notifiers.append( telegram )
