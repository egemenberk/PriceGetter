# -*- coding: utf-8 -*-
import time
import telebot
import logging
import sys
sys.path.insert(0, './../')
from item import Item
import validators
import database as db

commands = {
	"start": "Registers you to the system",
	"help": "Shows this message",
	"add": "Adds new product to your list",
	"fetch": "Fetch prices of the items in list"
}

class User:

    def __init__(self, user_id, name=''):
        self.id = user_id
        self.user_name = name

        # Item objects

        self.item_list = []

    def add_item(self, url):
        print("New item is added to user: " + str(self.id))
        item = Item(url)
        item.extract_info() # fetch soup and then name, price etc..
        db.ItemDb.get_or_create(owner=self.id, name=item.name, price=int(item.price), url=item.url)
        self.item_list.append(item)

    def check_prices(self):
        updated_items = []
        for item in self.item_list:
            old_price = item.price
            item.update()
            if old_price != item.price:
                updated_items.append(item)
        notify_user(updated_items)

    def get_prices(self):

        if len(self.item_list) == 0:
            self.get_items()

        result = []
        for item in self.item_list:
            result.append("Price of the item is ₺" + str(int(item.price)))
        if len(result) == 0:
            return "You have not added any item, type /add url"
        return "".join(result)

    def get_item_names(self):

        if len(self.item_list) == 0:
            self.get_items()

        result = []
        for i in range(len(self.item_list)):
            item = self.item_list[i]
            result.append(str(i+1) + "-) " + item.name[:25] + "\n")
        if len(result) == 0:
            return "You have not registered any item"
        return "".join(result)

    def get_items(self):
        """ Get items from database and save in self.item_list
        """
        item_list = db.get_user_items(self.id)
        for item in item_list:
            custom_item = Item(item.url, item.name, item.price)
            self.item_list.append(custom_item)
        return self.item_list

class Server:

    def __init__(self, bot):
        self.users = {}  # id, User
        self.bot = bot

    def get_or_create_user(self, user_id, name):
        user, created = db.UserDb.get_or_create(id=user_id, name=name)
        custom_user = User(user.id, user.name)
        self.users[user.id] = custom_user
        custom_user.get_items()

    def ask_name(self, message):
        name = message.text

    def is_registered(self, user_id):
        try:
            self.users[user_id]
        except KeyError:
            return False
        return True

    def get_user(self, user_id):
        if self.is_registered(user_id):
            return self.users[user_id]
        else:
            user = db.get_user(user_id)
            if user:
                custom_user = User(user_id, user.name)
                self.users[user_id] = custom_user
                return custom_user
            return None


token = open('token', 'r').read().strip()
bot = telebot.TeleBot(token)
server = Server(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    if server.is_registered(user_id):
        bot.send_message(message.chat.id, "You've already registered")

    server.get_or_create_user(user_id, name)
    bot.reply_to(message,
                 "Hello " + name )
    bot.send_message(message.chat.id,
                     "You can use /help command to learn how to use this bot")


@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"

    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['add'])
def add_item(message):
    user = server.get_user(message.from_user.id)
    url = message.text.replace(" ", "").replace("/add", "")

    if validators.url(url):
        user.add_item(url)
    else:
        bot.reply_to(message, "URL you've provided is wrong, please try again")


@bot.message_handler(commands=['delete'])
def delete_item(message):
    pass


@bot.message_handler(commands=['list'])
def list_items(message):
    user = server.get_user(message.from_user.id)
    if user == None:
        echo_all(message)
        return
    items = user.get_item_names()
    bot.send_message(message.chat.id, items)

def check_registered(func):
    def wrapper_check(*args, **kwargs):
        if user == None:
            echo_all(message)
            return
        func(*args, **kwargs)
    return wrapper_check


#TODO
@bot.message_handler(commands=['fetch'])
def notify_user(message):
    """ Notify user when price of any item is changed
    """
    user = server.get_user(message.from_user.id)
    if user == None:
        echo_all(message)
        return
    prices = user.get_prices()
    bot.reply_to(message, prices)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if server.is_registered(message.from_user.id) != True:
        bot.reply_to(message, 'Please write /start to register')
    else:
        bot.reply_to(message, "I don't know what you're talking about")
        command_help(message)


while True:
    logging.basicConfig(filename="log",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        if err == KeyboardInterrupt:
            break
        logging.error(err)
        time.sleep(5)
        print('Internet Error happened')

