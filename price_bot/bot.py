import logging
import validators
import database as db
import sys
sys.path.insert(0, './../')
sys.path.insert(0, "./../utils")

from telegram import Bot, ParseMode, ChatAction
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from item import Item, NAME_TAGS
from user import User
from server import Server
from proxy import get_proxies
from functools import wraps

NAME = 0
token = open('token', 'r').read().strip()

bot = Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

logging.basicConfig(filename="log", level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

server = Server()
proxies = get_proxies()


def callback_alarm(context : CallbackContext):
    """ This is called every specified minutes to
    notify users if any item in their watchlist changes
    """
    for user_id, user in server.users.items():
        updated_items = user.check_prices()
        if updated_items != "":
            context.bot.send_message(chat_id=user_id,
                                     text=updated_items,
                                     parse_mode=ParseMode.MARKDOWN)
        else:
            return None
            # DEBUG
            context.bot.send_message(chat_id=user_id,
                                     text="No change in item prices")


def send_typing_action(func):
    """Sends typing action while processing func command."""
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def reply(update, text, markdown=False):
    if markdown:
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(text)


@send_typing_action
def support_list(update, context):
    """ Command for showing supported websites
    """
    result = []

    for key, value in NAME_TAGS.items():
        result.append(key + "\n")

    reply(update, "".join(result))


@send_typing_action
def helper(update, context):
    help_text = "The following commands are available: \n"

    """ The below text is added to bot via BotFather using /setcommands
    help - Shows usages of the commands
    add - Adds new product to your list
    list - Fetches prices of the items in your list
    delete - Delete specified item with item_no in list
    support - Shows supported sites
    """

    commands = {
        "start": "Registers you to the system",
        "help": "Shows this message",
        "add": "Usage: /add NAME url or /add url",
        "list": "Fetches prices of the items from your list",
        "delete": "Usage: /delete item_no, you should provide item_no from the list you get by typing /list command",
        "support": "List supported sites to fetch prices of the items"
    }

    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"

    reply(update, help_text)  # send the generated help page


def start(update, context):
    user_id = update.message.chat_id

    if server.is_registered(user_id):
        reply(update, "You've already registered")
        return

    reply(update, "Hello, welcome to the PriceGetter Bot\n"
                              +"What is your name?" )

    return NAME


@send_typing_action
def name(update, context):
    user_id = update.message.chat_id
    name = update.message.text
    server.create_user(user_id, name)

    reply(update, "Hello " + name
                + ", you are registered now\n"
                + "You can start adding items to your "
                + "list by typing /add url\n"
                + "You can also use /help command "
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
@send_typing_action
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
@send_typing_action
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
        if "www." not in url:
            reply(update, "Add www before site_name")
            return
        elif user.add_item(url, item_name, proxies):
            reply(update, "You've already added this item")
        else:
            reply(update, "Your item has been successfully added")
    else:
        reply(update, "URL you've provided is wrong, please try again")


@must_register_first
@send_typing_action
def list_items(update, context):
    user_id = update.message.chat_id
    user = server.get_user(user_id)
    items = user.get_item_list()
    reply(update, items, markdown=True)


@send_typing_action
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

    #dispatcher.add_handler(start_handler)
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
