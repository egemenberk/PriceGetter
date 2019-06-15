import sys

list_of_price_files = sys.argv[1:]
prices = {}

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

get_prices(prices)
bigger_file = find_bigger_price_list(prices)
price_dict = prices[bigger_file]
print("\t" + bigger_file, end="")
for price_file_name in list_of_price_files:
    if price_file_name != bigger_file:
        print("\t" + price_file_name, end="")
print()
for name, price in price_dict.items():
    other_prices = []
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
    print(name[:20] + ": " + price.replace("\n","").replace("\xa0", "") + "\t", end='', flush=True)
    for other_price in other_prices:
        print(other_price.replace("\n", "").replace("\xa0", "") + "\t", end='', flush=True)
    print()
