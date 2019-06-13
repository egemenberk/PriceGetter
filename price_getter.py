import requests
from bs4 import BeautifulSoup
import random
import sys
from datetime import datetime

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

NAME_TAGS = {"vatanbilgisayar":  ["div", "id", "plhUrunAdi"],
             "hepsiburada": ["span", "itemprop","name"],
             "qp" : ["span", "class", "base"],
             "amazon": ["span", "id", "productTitle"],
             "ebrarbilgisayar": ["h1", "itemprop", "name"],
             "incehesap": ["h1", "itemprop", "name"],
             "trendyol": ["div", "class", "pr-in-nm"],
             "itopya": ["h1", "class", "name"],
             }

PRICE_TAGS = {"vatanbilgisayar":  ["span", "class", "ems-prd-price-selling"],
             "hepsiburada": ["span", "data-bind", "markupText:'currentPriceBeforePoint'"],
             "qp" : ["span", "class", "price"],
             "amazon": ["span", "id", "priceblock_ourprice"],
             "ebrarbilgisayar": ["div", "class", "urun_fiyati"],
             "incehesap": ["span", "class", "cur"],
             "trendyol": ["span", "class", "prc-slg"],
             "itopya": ["div", "class", "new text-right"]
             }

class PriceGetter:
    def __init__(self, url_list=[]):
        self.url_list = url_list
        self.price_list = {}
        self.soup_list = []

    # override for each website
    def get_name(self, soup, tag_list):
        name_holder = soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        return name_holder.text.strip()

    # override for each website
    def get_price(self, soup, tag_list, site_name):
        price_holder = soup.find(tag_list[0], {tag_list[1] : tag_list[2]})

        if "vatanbilgisayar" in site_name:
            return price_holder.text.split("TL")[0] + "TL"

        elif "itopya" in site_name:
            return price_holder.contents[0] + " TL"

        elif "hepsiburada" in site_name:
            return price_holder.text.strip() + " TL"

        elif "qp" in site_name:
            return price_holder.text.strip()

        elif "trendyol" in site_name:
            return price_holder.text.strip() + " TL"

        elif "incehesap" in site_name:
            return price_holder.text.strip('\r').replace(" ", "")

        elif "ebrar" in site_name:
            return price_holder.text.strip()

        elif "amazon" in site_name:
            return price_holder.text.strip() + " TL"

        else:
            print("You should not see this")

    def fetch_site_name(self, url):
        #url = json.loads(soup.find('script', type='application/ld+json').text)["url"]
        site_name = url.split(".com")[0].split("//www.")[1]
        return site_name

    def get_soups(self):
        random.shuffle(user_agent_list)
        headers = {"User-Agent": user_agent_list[0]}
        for url in self.url_list:
            page = requests.get(url, headers=headers)
            while page.status_code != 200:
                shuffle(user_agent_list)
                headers = {"User-Agent": user_agent_list[0]}
                page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            self.get_results(soup, url)

    def read_urls(self, filename):
        with open(filename, "r") as url_file:
            for line in url_file:
                self.url_list.append(line.rstrip())

    def __str__(self):
        prices = ""
        for key, value in self.price_list.items():
            prices += key + ": " + value + "\n"
        return prices

    def get_results(self, soup, url):
        site_name = self.fetch_site_name(url)
        tag_list = NAME_TAGS[site_name]
        name = self.get_name(soup, NAME_TAGS[site_name]) + "(" + site_name + ")"
        price = self.get_price(soup, PRICE_TAGS[site_name], site_name)
        print(name, price)
        self.price_list[name] = price

    def save_results(self, filename):
        day = datetime.now().strftime("%d-%m-%Y")
        out = open(filename.strip(".txt") + "-" + day + ".txt", "w+")
        for key, value in self.price_list.items():
            out.write(key + ":" + value + "\n")
        out.close()

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Usage is python3 price_getter.py <url_file>")
        exit(0)
    item = PriceGetter()
    item.read_urls(sys.argv[1])
    item.get_soups()
    item.save_results(sys.argv[1])
    #print(item)
