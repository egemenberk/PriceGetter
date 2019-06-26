import requests
from bs4 import BeautifulSoup
from item import *
from item_db import ItemDb

class Page():
    def __init__(self, url, category=None, proxies={}):
        self.url = url
        self.soup = None
        self.items = []
        self.category = category
        self.proxies = proxies

    def fetch_page(self):
        try:
            page = requests.get(self.url)
            self.soup = BeautifulSoup(page.text, 'html.parser')
            return self.soup
        except Exception as e:
            print(e)

        for url, val in self.proxies.items():
            print("Trying with new proxy:", url)
            try:
                page = requests.get(page_url, proxies= {val[0]: url}, timeout=1)
                self.soup = BeautifulSoup(page.text, 'html.parser')
                return self.soup
            except Exception as e:
                print(e)
                continue
            break
        return None

    def fetch_items(self):
        products = self.soup.find_all("div", {"class":"ems-prd-inner"})
        list_of_items = []
        for soup in products:
            item = Item(url=self.url, soup=soup)
            item.extract_info() # Get item item name, url and price
            if item.name == None: # Unnecessary items in page
                print("EMPTY NAME")
                continue
            #self.items.append(item)
            ItemDb.create(url=item.url, name=item.name, price=item.price, category=self.category)

