import requests
from bs4 import BeautifulSoup
from price_getter import PriceGetter

class Amazon(PriceGetter):
    def __init__(self, url_list=[]):
        super().__init__(url_list)

    def get_name(self, soup):
        name_holder = soup.find('span', {"id" :"productTitle"})
        return name_holder.text.strip()

    def get_price(self, soup):
        price_holder = soup.find('span', {"id" :"priceblock_ourprice"})
        return price_holder.text.strip() + " TL"

items = Amazon()
items.read_urls("amazon_prices.txt")
items.get_soups()
items.update()
print(items)
