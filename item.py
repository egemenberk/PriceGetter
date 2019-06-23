import requests
from bs4 import BeautifulSoup

NAME_TAGS = {"vatanbilgisayar":  ["div", "id", "plhUrunAdi"],
             "hepsiburada": ["span", "itemprop","name"],
             "qp" : ["span", "class", "base"],
             "amazon": ["span", "id", "productTitle"],
             "ebrarbilgisayar": ["h1", "itemprop", "name"],
             "incehesap": ["h1", "itemprop", "name"],
             "trendyol": ["div", "class", "pr-in-nm"],
             "itopya": ["h1", "class", "name"],
             "sinerji": ["h1", "itemprop", "name"],
             "gameekstra": ["div", "id", "urun_adi"]
             }

PRICE_TAGS = {"vatanbilgisayar":  ["span", "class", "ems-prd-price-selling"],
             "hepsiburada": ["span", "id", "offering-price"],
             "qp" : ["span", "class", "price"],
             "amazon": ["span", "id", "priceblock_ourprice"],
             "ebrarbilgisayar": ["div", "class", "urun_fiyati"],
             "incehesap": ["span", "class", "cur"],
             "trendyol": ["span", "class", "prc-slg"],
             "itopya": ["div", "class", "new text-right"],
             "sinerji": ["div", "class", "urun_fiyati"],
             "gameekstra": ["div", "id", "indirimli_cevrilmis_fiyat"]
             }

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("EXCEPTION occured in function" + str(func))
            print(e)
    return wrapper

class Item:
    def __init__(self, url=None, name="", price=0):
        self.url = url
        self.name = name
        self.price = price
        self.soup = None
        # From which tags to get price info
        self.price_tag_list = None
        self.name_tag_list = None
        # Stripped site name
        self.site_name = None

    def fetch_soup(self, headers=None):
        try:
            page = requests.get(self.url, headers=headers)
        except Exception as e:
            print("EXCEPTION occured while fetching soup")
            print(e)
            return None
        self.soup = BeautifulSoup(page.text, 'html.parser')
        return "success"

    def fetch_tags(self):
        self.name_tag_list = NAME_TAGS[self.site_name]
        self.price_tag_list = PRICE_TAGS[self.site_name]

    def fetch_site_name(self):
        self.site_name = self.url.split("www.")[1].split(".")[0]

    def get_name(self):
        tag_list = self.name_tag_list
        name_holder = self.soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        if name_holder == None:
            return "-"
        self.name = name_holder.text.strip() +  "(" + self.site_name + ")"

    def clean_price(self, price_holder):
        price = ""

        if price_holder == None:
            self.price = "0"
            return

        if "vatanbilgisayar" in self.site_name:
            price = price_holder.text.split("TL")[0]

        elif "itopya" in self.site_name:
            price = price_holder.contents[0]

        elif "incehesap" in self.site_name:
            price = price_holder.text.strip('\r')

        elif "hepsiburada" in self.site_name:
            price = price_holder["content"]

        else:
            price = price_holder.text.strip()

        price = price.replace(" ", "").upper().replace("TL", "").replace("₺", "")
        price = price.replace("KDV", "").replace("DAHIL", "")
        price = price.replace("\xa0", "").replace("\n", "")
        return price

    @handle_exception
    def get_price(self):
        tag_list = self.price_tag_list
        price_holder = self.soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        self.price = self.clean_price(price_holder)

    def extract_info(self):
        self.fetch_site_name()
        self.fetch_tags()
        self.get_name()
        self.get_price()
        print(self.name, self.price)

