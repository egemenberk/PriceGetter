import requests
from bs4 import BeautifulSoup
from price_getter import PriceGetter

class Hepsiburada(PriceGetter):
    def __init__(self, url_list=[]):
        super().__init__(url_list)

    def get_name(self, soup):
        name_holder = soup.find('span', {"itemprop" :"name"})
        print(soup.title)
        return name_holder.text

    def get_price(self, soup):
        price_holder = soup.find('span', {"data-bind" :"markupText:'currentPriceBeforePoint'"})
        return price_holder.text + " TL"


items = Hepsiburada()
items.read_urls("hepsiburada_prices.txt")
items.get_soups()
items.update()
print(items)
