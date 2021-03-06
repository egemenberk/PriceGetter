
# What is this?
This is my simple and humble hobby project.

This repository holds the scripts that are used to keep track of items 
from various e-commerce websites 

Items can be tracked manually by providing a list of urls to the main script. Also, it can send an e-mail including the items which you provided.

Items can also be tracked via telegram bot which notifies if there is a change.

Fetching whole items on a website with each items' categories is also possible. (It is only tested for vatanbilgisayar.com)

List of available websites can be found by asking /support to the telegram bot or
search NAME_TAGS in this repository

# How did it start?
I wanted to build a PC with my friend, for that purpose we prepared a list of items, 
but the problem was we did not have enough time to monitor and update the prices of each item, 
Since there were too many different sites we did not want to download and register 
to each site's app, so we wanted a single application to track all these items from 
different websites. Frankly, this project was born because of mine laziness.

TLDR: I wanted to monitor prices of items for my custom build PC

# What is not provided in this repository?

This project is not aimed to search and find the cheapest product from the web by comparing each website, instead you provide the urls of those items/products and it notifies you when there is a price change

# price_getter.py
This is a generic script to scrape price information from websites.

It requires a single url or a file that contains bunch of urls as an input.
The result with item prices is saved in a file

# site_getter.py
This module fetches the site as whole along with categories inside

# utils/item_db.py
This module uses peewee ORM to save fetched products in sqlite database

# utils/proxy.py
This scipt fetches available proxies to be later used with requests.get()
Because some sites ban abusive scraping methods that we are using with multiple threads

# utils/mail.py
This module is used for sending the prices of the items which are
fetched by the price_getter module.

# utils/list_prices
This module provides beautiful way to represent fetched results of the items
It takes bunch of text files that are generated by the price_getter module
Since price_getter now sends e-mails it is not being used and maintened any more

# price_bot
This is telegram bot, that is capable of keeping track of the items that
are provided by the user through telegram client. It notifies the user if
price of any item changes.

# Requirements
    pip3 install beautifulsoup4

## For price_bot
    pip3 install peewee
    pip3 install validators
    pip3 install python-telegram-bot==12.0.0b1 --upgrade

# Usage 
    python3 price_getter.py <file containing prices>

# PriceGetter Bot
To start using the bot [Click me](https://t.me/PriceGetter_bot)


![](https://media.giphy.com/media/LOnrqpjMZraIn14M0u/giphy.gif)

