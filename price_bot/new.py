import time
import telebot
import logging
import sys
sys.path.insert(0, './../')
from item import Item

class User:
	def __init__(self, user_id, name=""):
		self.id = user_id
		self.user_name = name
		# Item objects 
		self.item_list = []
	
	def add_item(self, url):
		self.item_list.append(Item(url))

	def check_prices():
		updated_items = []
		for item in self.item_list:
			old_price = item.price
			item.update()
			if old_price != item.price:
				updated_items.append(item)
		notify_user(updated_items)

class Server:
	def __init__(self, bot):
		self.users = {} # id, User
		self.bot = bot

	def create_user(self, user, name):
		new_user = User(user.id, name)
		if new_user not in self.users:
			print("Creating new user with id", new_user.id)
			self.users[user.id] = new_user

	def ask_name(self, message):
		name = message.text

	def is_registered(self, user_id):
        try:
            self.users["user_id"]
	    except KeyError:
            return False
        return True

token = open('token','r').read().strip()
bot = telebot.TeleBot(token)
server = Server(bot)

@bot.message_handler(commands=['dolar', "dol"])
def dolar(message):
    bot.reply_to(message, "Hello world")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello I'm price getter bot,\n What is yout name?")
	server.create_user(user=message.from_user, name=message.text)
	

@bot.message_handler(commands=['start', 'help'])
def add_item(message):
    
@bot.message_handler(commands=['update'])
def notify_user(message):
	""" Notify user when price of any item is changed
	"""

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	if server.is_registered(message.from_user.id) != True:
		bot.reply_to(message, "Please write /start to register")
	else:
		bot.reply_to(message, "I don't know what you're talking about")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        if (err == KeyboardInterrupt):
            break
        logging.error(err)
        time.sleep(5)
        print("Internet Error happened")
