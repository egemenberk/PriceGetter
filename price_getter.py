import requests
from bs4 import BeautifulSoup
import random
import sys
from datetime import datetime
import threading

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

thread_no = 16

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

class PriceGetter:
    def __init__(self, url_list=[]):
        self.url_list = url_list
        self.price_list_lock = threading.Lock()
        self.price_list = {}
        self.soup_list = []
        self.user_agent_list = user_agent_list

    # override for each website
    def get_name(self, soup, tag_list):
        name_holder = soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        if name_holder == None:
            return "-"
        return name_holder.text.strip()

    def clean_price(self, price):
        price = price.replace(" ", "").upper().replace("TL", "").replace("₺", "")
        price = price.replace("KDV", "").replace("DAHIL", "")
        return price

    # override for each website
    def get_price(self, soup, tag_list, site_name):
        price_holder = soup.find(tag_list[0], {tag_list[1] : tag_list[2]})
        price = ""

        if price_holder == None:
            return "-"

        if "vatanbilgisayar" in site_name:
            price = price_holder.text.split("TL")[0]

        elif "itopya" in site_name:
            price = price_holder.contents[0]

        elif "incehesap" in site_name:
            price = price_holder.text.strip('\r')

        elif "hepsiburada" in site_name:
            price = price_holder["content"]

        else:
            price = price_holder.text.strip()

        return self.clean_price(price)

    def fetch_site_name(self, url):
        #url = json.loads(soup.find('script', type='application/ld+json').text)["url"]
        site_name = url.split("www.")[1].split(".")[0]
        return site_name

    def get_soups(self):
        list_of_url_lists = split(self.url_list, thread_no)
        threads = []
        for url_list in list_of_url_lists:
            t = threading.Thread(target=self.get_soups_helper, args=(url_list, ))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def new_header(self):
        random.shuffle(self.user_agent_list)
        headers = {"User-Agent": user_agent_list[0]}
        return headers

    def get_soups_helper(self, url_list):
        headers = self.new_header()
        for url in url_list:
            page = requests.get(url, headers=headers)
            while page.status_code != 200:
                headers = self.new_header()
                try:
                    page = requests.get(url, headers=headers)
                except Exception as e:
                    print(e)
                    headers = self.new_header()
            soup = BeautifulSoup(page.text, 'html.parser')
            self.extract_items(soup, url)

    def read_urls(self, filename):
        with open(filename, "r") as url_file:
            for line in url_file:
                self.url_list.append(line.rstrip())

    def __str__(self):
        prices = ""
        for key, value in self.price_list.items():
            prices += key + ": " + value + "\n"
        return prices

    def extract_items(self, soup, url):
        site_name = self.fetch_site_name(url)
        tag_list = NAME_TAGS[site_name]
        name = self.get_name(soup, NAME_TAGS[site_name]) + "(" + site_name + ")"
        price = self.get_price(soup, PRICE_TAGS[site_name], site_name)
        print(name, price)
        with self.price_list_lock:
            self.price_list[name] = price

    def save_results(self, filename):
        day = datetime.now().strftime("%d-%m-%Y")
        out = open(filename.strip(".txt") + "-" + day + ".txt", "w+")
        for key, value in self.price_list.items():
            out.write(key + ":" + value + "\n")
        out.close()

def help():
    print("\nusage: python3 price_getter.py [-h] [--url] [files] [url] \n")
    print("Arguments")
    print("\t -u or --url <url>:\t Fetch the price from given url")
    print("\t -f or --file <price file>:\t Fetch prices from given file")
    print("\t -h or --help:\t Show this help info")

    if(len(sys.argv) < 2):
        print("python3 price_getter.py --help or -h for more info")
        exit(0)

if __name__ == '__main__':

    if len(sys.argv) > 3:
        help()
        exit()

    arg = sys.argv[1]

    if arg == "-u" or arg == "--url":
        index_url = sys.argv.index(arg) + 1
        url_list = []
        try:
            url_list.append(sys.argv[index_url])
        except IndexError:
            help()
            exit(0)

        item = PriceGetter(url_list)
        item.get_soups()
        exit(0)

    if arg == "-f" or arg == "--file":
        file_loc = sys.argv.index(arg) + 1
        filename = ""
        try:
            filename = sys.argv[file_loc]
        except:
            help()
            exit(0)

        item = PriceGetter()
        item.read_urls(filename)
        item.get_soups()
        item.save_results(sys.argv[1])

    else:
        help()
        exit(0)
