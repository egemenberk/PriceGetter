import requests
from bs4 import BeautifulSoup
from price_getter import PriceGetter

class Itopya(PriceGetter):
    def __init__(self, url_list=[]):
        super().__init__(url_list)

    def get_name(self, soup):
        name_holder = soup.find('h1', {"class" :"name"})
        return name_holder.text.strip()

    def get_price(self, soup):
        price_holder = soup.find('div', {"class" :"new text-right"})
        return price_holder.contents[0] + " TL"


items = Itopya()
items.read_urls("itopya_prices.txt")
items.get_soups()
items.update()
print(items)
