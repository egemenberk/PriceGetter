import logging
import telegram

logging.basicConfig(filename="log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import time
import sys
sys.path.insert(0, './../')
from item import Item
import validators
import database as db
from user import User
from server import Server

token = open('token', 'r').read().strip()
bot = Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

server = Server()

def callback_alarm(context: telegram.ext.CallbackContext):
    user_id = context.job.context
    user = server.get_user(user_id)
    updated_items = user.check_prices()

    if len(updated_items):
        context.bot.send_message(chat_id=context.job.context,
                                 text=updated_items)
    else:
        context.bot.send_message(chat_id=context.job.context,
                                 text="No change in item prices")


def callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='I will notify if price of any item changes!')
    hour = 10
    context.job_queue.run_repeating(callback_alarm, hour, context=update.message.chat_id)


def reply(update, text):
    update.message.reply_text(text)


def helper(update, context):
    help_text = "The following commands are available: \n"

    commands = {
	"start": "Registers you to the system",
	"help": "Shows this message",
	"add": "Adds new product to your list",
	"list": "Fetches prices of the items in list"
    }

    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    reply(update, help_text)  # send the generated help page


def start(update, context):
    user_id = update.message.chat_id
    name = update.message.chat.first_name
    server.get_or_create_user(user_id, name)

    if server.is_registered(user_id):
        update.message.reply_text("You've already registered")
        return

    update.message.reply_text("You can use /help command to learn how to use this bot")


def add(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    try:
        url = context.args[0].replace(" ", "").replace("/add", "")
    except:
        reply(update, "Usage: /add url")
        return
    if validators.url(url):
        user.add_item(url)
    else:
        reply(update, "URL you've provided is wrong, please try again")

def list_items(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    if user == None:
        echo_all(update, context)
        return
    items = user.get_item_list()
    reply(update, items)


def echo(update, context):
    if server.is_registered(message.from_user.id):
        reply(update, "I don't know what you're talking about")
    else:
        reply(update, "Please write /start to register")


list_item_handler = CommandHandler('list', list_items)
echo_handler = CommandHandler('echo', echo)
start_handler = CommandHandler('start', start)
add_item_handler = CommandHandler('add', add)
help_handler = CommandHandler('help', helper)
timer_handler = CommandHandler('notify', callback_timer)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_item_handler)
dispatcher.add_handler(list_item_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(timer_handler)
updater.start_polling()
