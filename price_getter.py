#!/usr/bin/env python3
from bs4 import BeautifulSoup
import random
import sys
from datetime import datetime
import threading
import argparse
from item import Item
import os

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

thread_number = 16

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Fetch the price from given url")
    parser.add_argument("-f", "--file", help="Fetch prices from given file")
    args = parser.parse_args()
    return args

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class PriceGetter:
    def __init__(self, item_list=[]):
        self.item_list = item_list
        self.price_list_lock = threading.Lock()
        self.price_list = {}
        self.user_agent_list = user_agent_list
        self.headers = {"User-Agent": user_agent_list[0]}

    def get_soups(self, thread_number):
        list_of_item_lists = split(self.item_list, thread_number)
        threads = []
        for item_list in list_of_item_lists:
            t = threading.Thread(target=self.get_soups_helper, args=(item_list, ))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def generate_new_header(self):
        random.shuffle(self.user_agent_list)
        self.headers = {"User-Agent": user_agent_list[0]}

    def get_soups_helper(self, item_list):
        for item in item_list:
            while item.fetch_soup(self.headers) == None:
                self.generate_new_header()
            item.extract_info()
            with self.price_list_lock:
                self.price_list[item.name] = item.price

    def read_urls(self, filename):
        with open(filename, "r") as url_file:
            for line in url_file:
                item = Item(line.rstrip())
                self.item_list.append(item)

    def __str__(self):
        prices = ""
        for key, value in self.price_list.items():
            prices += key + ": " + value + "\n"
        return prices

    def save_results(self, filename):
        if "results" not in os.listdir("."):
            os.makedirs("results")
        day = datetime.now().strftime("%d-%m-%Y")
        out = open("results/" + day + ".txt", "w+")
        for key, value in self.price_list.items():
            out.write(key + ":" + value + "\n")
        out.close()

if __name__ == '__main__':

    args = handle_args()

    if args.url != None:
        item_list = []
        item_list.append(Item(args.url))
        items = PriceGetter(item_list)
        items.get_soups(thread_number=1)

    if args.file != None:
        filename = args.file
        item = PriceGetter()
        item.read_urls(filename)
        item.get_soups(thread_number=thread_number)
        item.save_results(filename)


