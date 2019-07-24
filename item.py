import requests
import re
import random
from bs4 import BeautifulSoup
from user_agents import get_new_header
import logging

URL_TAGS = {"vatanbilgisayar":  ["div", "class", "ems-prd-name"]

            }

NAME_TAGS = {"vatanbilgisayar.com":  ["div", "class", "ems-prd-name"],
             "hepsiburada.com": ["span", "itemprop","name"],
             "qp.com.tr" : ["span", "class", "base"],
             "amazon.com.tr": ["span", "id", "productTitle"],
             "ebrarbilgisayar.com": ["h1", "itemprop", "name"],
             "incehesap.com" : ["h1", "itemprop", "name"],
             "trendyol.com": ["div", "class", "pr-in-nm"],
             "itopya.com": ["h1", "class", "name"],
             "sinerji.gen.tr": ["h1", "itemprop", "name"],
             "gameekstra.com": ["div", "id", "urun_adi"],
             "urun.n11.com": ["div", "class", "nameHolder"],
             "m.n11.com": ["h1", "class", "title"],
             "amazon.com": ["span", "id", "productTitle"],
             "newegg.com": ["span", "itemprop", "name"],
             "ebay.com": ["h1", "itemprop", "name"],
             "mediamarkt.com.tr": ["h1", "itemprop", "name"],
             "teknosa.com": ["div", "class", "product-title"],
             "istanbulbilisim.com": ["h1", "itemprop", "name"]
             }

PRICE_TAGS = {"vatanbilgisayar.com":  ["span", "class", "ems-prd-price-selling"],
             "hepsiburada.com": ["span", "id", "offering-price"],
             "qp.com.tr" : ["span", "class", "price"],
             "amazon.com.tr": ["span", "id", "priceblock_ourprice"],
             "ebrarbilgisayar.com": ["div", "class", "urun_fiyati"],
             "incehesap.com": ["span", "class", "cur"],
             "trendyol.com": ["span", "class", "prc-slg"],
             "itopya.com": ["div", "class", "new text-right"],
             "sinerji.gen.tr": ["div", "class", "urun_fiyati"],
             "gameekstra.com": ["div", "id", "indirimli_cevrilmis_fiyat"],
             "urun.n11.com": ["div", "class", "newPrice"],
             "m.n11.com": ["ins", "class", "price"],
             "amazon.com": ["span", "id", "priceblock_ourprice"],
             "newegg.com": ["li", "class", "price-current"],
             "ebay.com": ["span", "id", "mm-saleDscPrc"],
             "mediamarkt.com.tr": ["meta", "itemprop", "price"],
             "teknosa.com": ["div", "class", "price-tag"],
             "istanbulbilisim.com": ["p", "class", "price-act"]
             }


class Item:
    def __init__(self, url=None, name=None, price=0, soup=None):
        self.url = url
        self.name = name
        self.price = price
        self.soup = soup
        # From which tags to get price info
        self.price_tag_list = None
        self.name_tag_list = None
        self.url_tags = None
        # Stripped site name
        self.site_name = None

    def update(self):
        self.extract_info()

    def fetch_soup(self, proxies={}):
        headers = get_new_header()
        try:
            page = requests.get(self.url) # FUCKING HEADERS CHANGE THE SITE, headers=headers)
            if page.status_code > 500:
                print("Server Error")
            else:
                self.soup = BeautifulSoup(page.text, 'html.parser')
                title = self.soup.title.text
                if title != "Are you a human?" and title != "Robot Check":
                    return 1

        except Exception as e:
            print("EXCEPTION occured while fetching soup")
            print(e)
            return None

        for url, val in proxies.items():
            #print("Trying with new proxy:", url)
            headers = get_new_header()
            try:
                page = requests.get(self.url, proxies= {val[0]: url},
                                    timeout=1,
                                    headers=headers)
                if page.status_code > 500:
                    print("Server Error")
                    continue

                self.soup = BeautifulSoup(page.text, 'html.parser')
                title = self.soup.title.text
                if title != "Are you a human?" and title != "Robot Check":
                    return 1

            except Exception as e:
                logging.exception("with proxy in fetch_page")
                #print(e)
                continue

        return 1

    def fetch_tags(self, url_set):
        self.name_tag_list = NAME_TAGS[self.site_name]
        self.price_tag_list = PRICE_TAGS[self.site_name]
        if url_set == False:
            self.url_tags = URL_TAGS[self.site_name]

    def fetch_site_name(self):
        if "www." in self.url:
            self.site_name = self.url.split("www.")[1].split("/")[0]
        else: # Some fucking sites having fucking names
            raise Exception

    def get_url(self):
        url = self.soup.find(self.url_tags[0], {self.url_tags[1]:self.url_tags[2]})
        if url == None:
            self.url = None
        if url.find("a") == None:
            self.url = None
        self.url = url.find("a")["href"]

    def get_name(self):
        if self.site_name == "ebay.com":
            self.name = self.soup.title.text
            return
        if self.name != None:
            return
        tag_list = self.name_tag_list
        name_holder = self.soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        if name_holder == None:
            self.name = "Name couldn't fetched"
            return
        self.name = name_holder.text.strip() +  "(" + self.site_name + ")"

    def clean_price(self, price_holder):
        """Remove unnecessary strings from price"""
        price = ""

        if price_holder == None:
            self.price = "0"
            return

        if self.site_name == None:
            self.fetch_site_name()

        if "vatanbilgisayar.com" in self.site_name:
            price = price_holder.text.split("TL")[0]

        elif "itopya.com" in self.site_name:
            price = price_holder.contents[0]

        elif "incehesap.com" in self.site_name:
            price = price_holder.text.strip('\r')

        elif "hepsiburada.com" in self.site_name:
            price = price_holder["content"]

        elif "mediamarkt.com.tr" in self.site_name:
            price = price_holder["content"]

        else:
            price = price_holder.text.strip()

        price = price.replace(" ", "").upper().replace("TL", "").replace("₺", "")
        price = price.replace("KDV", "").replace("DAHIL", "")
        price = price.replace("\xa0", "").replace("\n", "")
        self.price = price

    def convert_price(self):
        """Gets String Returns Float"""
        price = self.price.replace("\n", "").replace("\xa0","")
        num = re.search('[0-9]+[\.|\,]?[0-9]+', price)
        if num == None:
            price = 0
        else:
            price = float(num.group().replace(",", "."))
            if price < 10:
                price *= 1000
        self.price = price

    def get_price(self):
        tag_list = self.price_tag_list
        price_holder = self.soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        self.clean_price(price_holder)
        self.convert_price()

    def extract_info(self, url_set=True, proxies={}):
        """Extract name and price"""
        if self.soup == None:
            self.fetch_soup(proxies)
        self.fetch_site_name()
        self.fetch_tags(url_set)
        self.get_name()
        self.get_price()
        print(self.soup.find("span", {"id": "productTitle"}))
        print(self.site_name)
        print(self.name_tag_list, self.price_tag_list)
        print(self.name, self.price, url_set, len(proxies))
        if url_set == False:
            self.get_url()

