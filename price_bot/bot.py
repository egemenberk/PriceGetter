import logging
import telegram

logging.basicConfig(filename="log", level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
import time
import sys
sys.path.insert(0, './../')
sys.path.insert(0, "./../utils")
from item import Item, NAME_TAGS
import validators
import database as db
from user import User
from server import Server
from proxy import get_proxies

token = open('token', 'r').read().strip()
bot = Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

server = Server()
proxies = get_proxies()

def callback_alarm(context : telegram.ext.CallbackContext):
    """ This is called every specified minutes to
    notify users if any item in their watchlist changes
    """
    for user_id, user in server.users.items():
        updated_items = user.check_prices()
        if updated_items != "":
            context.bot.send_message(chat_id=user_id,
                                     text=updated_items,
                                     parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            return None
            # DEBUG
            context.bot.send_message(chat_id=user_id,
                                     text="No change in item prices")


def reply(update, text, markdown=False):
    if markdown:
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text(text)


def support_list(update, context):
    """ Command for showing supported websites
    """
    result = []

    for key, value in NAME_TAGS.items():
        result.append(key + "\n")

    reply(update, "".join(result))


def helper(update, context):
    help_text = "The following commands are available: \n"

    """
    help - Shows usages of the commands
    add - Adds new product to your list
    list - Fetches prices of the items in your list
    delete - Delete specified item with item_no in list
    """

    commands = {
        "start": "Registers you to the system",
        "help": "Shows this message",
        "add": "Usage: You can provide custom name by /add NAME url or /add url",
	"list": "Fetches prices of the items in list",
        "delete": "/delete item_no, you should provide item_no from the list you get by typing /list command"
    }

    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    reply(update, help_text)  # send the generated help page

NAME = 1

def start(update, context):
    user_id = update.message.chat_id

    if server.is_registered(user_id):
        update.message.reply_text("You've already registered")
        return

    update.message.reply_text("Hello, welcome to the PriceGetter Bot\n"
                              +"What is your name?" )

    return NAME


def name(update, context):
    user_id = update.message.chat_id
    name = update.message.text
    server.create_user(user_id, name)

    update.message.reply_text("Hello " + name
                              + ", You are registered now"
                              + ", you can start adding items to your "
                              + "list by typing /add url\n"
                              + ", you can also use /help command "
                              + "to learn how to use this bot")

    return ConversationHandler.END

def cancel(update, context):
    reply(update, 'Bye! I hope we can talk again some day.')
    return ConversationHandler.END

def must_register_first(func):
    def wrapper(*args, **kwargs):
        update = args[0]
        user_id = update.message.chat_id
        if server.is_registered(user_id) == False:
            reply(update, "You should register first by using /start")
        else:
            func(*args, **kwargs)
    return wrapper

@must_register_first
def delete(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    try:
        response = user.remove_item(int(context.args[0]))
        reply(update, response)
    except Exception as e:
        print(e)
        reply(update, "Usage: /delete item_no")


@must_register_first
def add(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    item_name = None
    if len(context.args) == 2:
        try:
            item_name = context.args[0]
            url = context.args[1].replace(" ", "").replace("/add", "")
        except:
            reply(update, "Usage: /add name url")
            return
    elif len(context.args) == 1:
        try:
            url = context.args[0].replace(" ", "").replace("/add", "")
        except:
            reply(update, "Usage: /add url")
            return
    elif len(context.args) == 0:
            reply(update, "Provide url, Usage: /add url")
            return
    else:
        reply(update, "Provide url, Usage: /add url")
        return

    if validators.url(url):
        if user.add_item(url, item_name, proxies):
            reply(update, "You've already added this item")
        else:
            reply(update, "Your item has been successfully added")
    else:
        reply(update, "URL you've provided is wrong, please try again")

@must_register_first
def list_items(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    items = user.get_item_list()
    reply(update, items, markdown=True)


def echo(update, context):
    if server.is_registered(message.from_user.id):
        reply(update, "I don't know what you're talking about")
    else:
        reply(update, "Please write /start to register")


if __name__ == '__main__':
    list_item_handler = CommandHandler('list', list_items)
    echo_handler = CommandHandler('echo', echo)
    start_handler = CommandHandler('start', start)
    add_item_handler = CommandHandler('add', add)
    help_handler = CommandHandler('help', helper)
    delete_handler = CommandHandler('delete', delete)
    suppor_list_handler = CommandHandler('support', support_list)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={ NAME: [MessageHandler(Filters.text, name)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_item_handler)
    dispatcher.add_handler(list_item_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(delete_handler)
    dispatcher.add_handler(suppor_list_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(conversation_handler)

    server.start()
    print("Server has started")
    ten_min = 5 * 60
    j.run_repeating(callback_alarm, interval=ten_min)

    updater.start_polling()
