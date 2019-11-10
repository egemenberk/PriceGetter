import sys
sys.path.append("../")
from item import *
import json

class Pc:
    def __init__(self):
        self.mb = [] # motherboards
        self.cpu = []
        self.gpu = []
        self.ssd = []
        self.psu = [] # power supply
        self.case = []

    def insert(self, url, attr):
        item = Item(url)
        item.fetch_soup()
        item.extract_info()
        dic = {"url":item.url, "name": item.name, "price": item.price}
        self.__getattribute__(attr).append(dic)
        sorted(self.__getattribute__(attr), key=lambda x:x["price"])

    def __str__(self):
        out = []
        total = 0
        for category in self.__dict__.keys():
            out.append(category)
            i = 0
            for item in self.__getattribute__(category):
                out.append(item["name"] + ": " + str(item["price"]))
                if i == 0 and item["price"] != 0:
                    total += item["price"]
                    i = 1
            out.append("----------------")
        out.append("Total: " + str(total))
        out.append("Note: Total is calculated by using the cheapest products")
        return "\n".join(out)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

select_table = {1: "cpu",
                2: "gpu",
                3: "ssd",
                4: "case",
                5: "mb",
                6: "psu"}

if __name__ == "__main__":
    pc = Pc()
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as read_file:
            saved = json.load(read_file)
            for key, val in saved.items():
                pc.__setattr__(key, val)

    while True:
        print()
        print("Please select category to insert item")
        print("1-) Cpu")
        print("2-) Gpu")
        print("3-) Ssd")
        print("4-) Case")
        print("5-) MotherBoard")
        print("6-) Psu")
        print("7-) List Items")
        print("8-) Save to a file")
        print("9-) Exit from program")

        selection = int(input())

        if selection < 7:
            print("Please provide URL for " + select_table[selection] + ": ")
            try:
                url = input()
            except:
                continue
            pc.insert(url, select_table[selection])

        elif selection == 7:
            print(pc)
            continue

        elif selection == 8:
            print("Enter file name: ")
            file_name = input()
            with open(file_name, "w") as filee:
                result = pc.toJSON()
                filee.write(result)

        elif selection == 9:
            exit(0)

        else:
            print("Provide valid selection")

