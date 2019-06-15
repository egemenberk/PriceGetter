import sys

list_of_price_files = sys.argv[1:]
print(list_of_price_files)
prices = {}

def read_prices(filename):
    prices = {}
    with open(filename, "r") as price_file:
        for line in price_file:
            name, price = line.split(":")
            prices[name] = price

    return prices

for price_file in list_of_price_files:
    prices[price_file] = read_prices(price_file)

price_dict = prices[list_of_price_files[0]]
for name, price in price_dict.items():
    other_prices = []
    for price_file_name in list_of_price_files[1:]:
        price_dict_other = prices[price_file_name]
        other_price = "0"
        try:
            other_price = price_dict_other[name]
        except KeyError:
            pass
        other_prices.append(other_price)
    print(name[:30] + ": " + price.replace("\n","").replace("\xa0", "") + "\t", end='', flush=True)
    for other_price in other_prices:
        print(other_price.replace("\n", "").replace("\xa0", "") + "\t", end='', flush=True)
    print()
