import atom.notify
import telegram
import os

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

print("Telegram module initializing.")

token_filepath = os.path.expanduser("~/.atomtoken")
chat_filepath = os.path.expanduser("~/.atomchat")
chat = int(open(chat_filepath).read())
REQUEST_KWARGS={
	'proxy_url': 'socks5://127.0.0.1:9050',
}

def filterchat(func):
	def decfunc(bot, update):
		if update.message.chat_id != chat:
			return
		return func(bot, update)

	return decfunc

@filterchat
def start(bot, update):	
	try:
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
		self.updater = Updater(bot=self.bot, request_kwargs = REQUEST_KWARGS)

		try:
			answer = self.bot.get_me()
			print("Telegram bot:", answer)
		except:
			print("Autorize telegram bot fault")

		start_handler = CommandHandler('start', start)
		self.updater.dispatcher.add_handler(start_handler)

		input_message_handler = MessageHandler(Filters.text, input_message)
		self.updater.dispatcher.add_handler(input_message_handler)

	def notify(self, text):
		self.bot.send_message(chat_id=chat, text=text)

	def start_polling(self):
		print("Telegram polling was started.")
		self.updater.start_polling(clean=True)
	
	def get_updates(self):
		updates = self.bot.get_updates()
		print([u.message.text for u in updates])

telegram = Telegram()
telegram.get_updates()
telegram.start_polling()
	
atom.notify.notifiers.append( telegram )

