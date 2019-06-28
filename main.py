#!/usr/bin/env python3
import argparse
import proxy
from website import Site
from category import Category

url = "https://www.vatanbilgisayar.com/"
next_page = "?page="

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--category", help="Fetch the prices from given category")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = handle_args()
    #proxies = proxy.working_proxies()
    site = Site(url, proxy_enabled=1, thread_no=12)

    if args.category == None:
        print("Provide category")
        exit(0)

    if args.category == "all":
        site.fetch_categories()

    else:
        category = Category(url + args.category, category=args.category, appendix="/?page=")
        site.categories.append(category)

    site.fetch_all()

