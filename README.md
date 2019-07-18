# price_getter.py
This is a generic script to scrape price information from websites
It requires a single url or a file that contains bunch of urls as an input
The result with item prices is saved in a file

# site_getter.py
This module fetches the site as whole along with categories inside.

# utils/item_db.py
This module uses peewee ORM to save fetched products in sqlite database.

# utils/proxy.py
This scipt fetches available proxies to be later used with requests.get()
Because some sites ban abusive scraping methods that we are using with threading

# utils/mail.py
This module is used for sending the prices of the items which are
fetched by the price_getter module.

# utils/list_prices
This module provides beautiful way to represent fetched results of the items

# price_bot
This is telegram bot, that is capable of keeping track of the items that
are provided by the user through telegram client

# Requirements
    pip3 install beautifulsoup4

## For price_bot
    pip3 install peewee
    pip3 install validators
    pip3 install python-telegram-bot==12.0.0b1 --upgrade

# Usage 
    python3 price_getter.py \<file containing prices\>

# PriceGetter Bot
To start using the bot [Click me](https://t.me/PriceGetter_bot)


![](https://media.giphy.com/media/LOnrqpjMZraIn14M0u/giphy.gif)

