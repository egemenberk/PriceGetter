#!/usr/bin/env python3
import sys
import re

def clean_price(price):
    """ Gets String Returns Float
    """
    price = price.replace("\n", "").replace("\xa0","")
    num = re.search('[0-9]+[\.|\,]?[0-9]+', price)
    if num == None:
        return 0
    else:
        price = float(num.group().replace(",", "."))
        if price < 10:
            return price * 1000
        return price

def read_prices(filename):
    prices = {}
    with open(filename, "r") as price_file:
        for line in price_file:
            name, price = line.split(":")
            prices[name] = price

    return prices

def get_prices(prices):
    for price_file in list_of_price_files:
        prices[price_file] = read_prices(price_file)

def find_bigger_price_list(prices):
    bigger_file = ""
    maxim = 0
    for key, val in prices.items():
        if len(val) > maxim:
            maxim = len(val)
            bigger_file = key
    return bigger_file

if __name__ == '__main__':
    list_of_price_files = sys.argv[1:]
    prices = {}
    get_prices(prices)
    bigger_file = find_bigger_price_list(prices)
    price_dict = prices[bigger_file]
    print("\t"*3 + bigger_file, end="")
    for price_file_name in list_of_price_files:
        if price_file_name != bigger_file:
            print("\t" + price_file_name, end="")
    print()
    i=0
    for name, price in price_dict.items():
        other_prices = [price]
        print("{})".format(i), end="")
        i+=1
        for price_file_name in list_of_price_files:
            if price_file_name == bigger_file:
                continue
            price_dict_other = prices[price_file_name]
            other_price = "0"
            try:
                other_price = price_dict_other[name]
            except KeyError:
                pass
            other_prices.append(other_price)
        print(name[:20] + ": ", end='', flush=True)
        for other_price in other_prices:
            print("{1:5.0f} {0:>10s} ".format("",clean_price(other_price)), end="")
        print()
