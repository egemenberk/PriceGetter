import sys
sys.path.append("../")
from item import *
import pickle

class Pc:
    def __init__(self):
        self.mb = [] # motherboards
        self.cpu = []
        self.gpu = []
        self.ssd = []
        self.case = []

    def insert(self, url, attr):
        item = Item(url)
        item.fetch_soup()
        item.extract_info()
        self.__getattribute__(attr).append(item)
        sorted(self.__getattribute__(attr), key=lambda x:x.price)

    def __str__(self):
        out = []
        total = 0

        for category in self.__dict__.keys():
            out.append(category)
            i = 0
            for item in self.__getattribute__(category):
                out.append(item.name + ": " + str(item.price))
                if i == 0 and item.price != 0:
                    total += item.price
                    i = 1
            out.append("----------------")
        out.append("Total: " + str(total))
        return "\n".join(out)

select_table = {1: "cpu",
                2: "gpu",
                3: "ssd",
                4: "case",
                5: "mb"}

if __name__ == "__main__":
    pc = None
    if len(sys.argv) == 2:
        pc = pickle.load(sys.argv[1])
    else:
        pc = Pc()
    while True:
        print()
        print("Please select option")
        print("1-) Cpu")
        print("2-) Gpu")
        print("3-) Ssd")
        print("4-) Case")
        print("5-) MotherBoard")
        print("6-) List Items")
        print("7-) Save to a file")
        print("8-) Exit from program")

        selection = int(input())

        if selection < 6:
            print("Please provide URL for " + select_table[selection] + ": ")
            try:
                url = input()
            except:
                continue
            pc.insert(url, select_table[selection])

        elif selection == 6:
            print(pc)
            continue

        elif selection == 7:
            print("Enter file name: ")
            file_name = input()
            with open(file_name, "wb") as filee:
                pickle.dump(pc, filee)

        elif selection == 8:
            exit(0)

        else:
            print("Provide valid selection")

