import requests
from bs4 import BeautifulSoup
from item import *
from item_db import ItemDb
import logging
import gc

class Page():
    def __init__(self, url, category=None, proxies={}, db_lock=None):
        self.url = url
        self.soup = None
        self.items = []
        self.category = category
        self.proxies = proxies
        self.db_lock = db_lock

    def fetch_page(self):
        try:
            page = requests.get(self.url)
            self.soup = BeautifulSoup(page.text, 'html.parser')
            return self.soup
        except Exception as e:
            logging.exception("first try in fetch_page")
            #print(e)

        for url, val in self.proxies.items():
            print("Trying with new proxy:", url)
            try:
                page = requests.get(self.url, proxies= {val[0]: url}, timeout=1)
                self.soup = BeautifulSoup(page.text, 'html.parser')
                return self.soup
            except Exception as e:
                logging.exception("with proxy in fetch_page")
                #print(e)
                continue
            break
        return None

    def fetch_items(self):
        products = self.soup.find_all("div", {"class":"ems-prd-inner"})
        for soup in products:
            item = Item(url=self.url, soup=soup)
            item.extract_info() # Get item item name, url and price
            if item.name == None: # Unnecessary items in page
                print("EMPTY NAME")
                continue
            #self.items.append(item)
            with self.db_lock:
                ItemDb.create(url=item.url, name=item.name, price=item.price, category=self.category)
            item = None
        products = None
        gc.collect()
