#!/usr/bin/env python3
from bs4 import BeautifulSoup
import random
import sys
from datetime import datetime
import threading
import argparse
from item import Item
import os
from item_db import ItemDb
sys.path.insert(0, "utils")
from mail import send_mail
from proxy import get_proxies


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
        self.db_lock = threading.Lock()

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

    def get_soups_helper(self, item_list):
        proxies = get_proxies()
        for item in item_list:
            status = item.fetch_soup(proxies=proxies)
            if status == None:
                self.item_list.remove(item)
                continue
            item.extract_info()
            with self.db_lock:
                ItemDb.create(url=item.url, name=item.name, price=item.price)

    def read_urls(self, filename):
        with open(filename, "r") as url_file:
            for line in url_file:
                item = Item(url=line.rstrip())
                self.item_list.append(item)

    def make_link(self, item):
        link = "<a href=" + item.url + ">" + item.name[:30] + "</a>" + ": " + str(item.price) + " TL<br>"
        return link

    def e_mail(self):
        prices = []
        for item in self.item_list:
            prices.append(self.make_link(item))
        day = datetime.now().strftime("%d-%m-%Y")
        message = "".join(prices)
        send_mail(message.encode("ascii", errors="ignore").decode(), day)

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
        item.e_mail()

