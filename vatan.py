import requests
from bs4 import BeautifulSoup
from price_getter import PriceGetter

class Vatan(PriceGetter):
    def __init__(self, url_list=[]):
        super().__init__(url_list)

    def get_name(self, soup):
        name_holder = soup.find('div', {"id" :"plhUrunAdi"})
        return name_holder.text.strip()

    def get_price(self, soup):
        price_holder = soup.find('span', {"class" :"ems-prd-price-selling"})
        return price_holder.text.split("TL")[0] + "TL"


items = Vatan()
items.read_urls("vatan_prices.txt")
items.get_soups()
items.update()
print(items)
