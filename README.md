# price_getter.py
This is a generic script to scrape price information from websites
It requires a single url or a file that contains bunch of urls as an input
The result is saved in a file

# item_db.py
This module uses peewee ORM to save fetched products in sqlite database.

# vatan.py
This script fetches list of products from a category or from all categories.

# proxy.py
This scipt fetches available proxies to be later used with requests.get()
Because some sites ban abusive scraping methods that we are using with threading

# Requirements
pip3 install beautifulsoup4

# Usage 
python3 price_getter.py \<file containing prices\>
