import database as db
import sys
sys.path.insert(0, './../')
sys.path.insert(0, './../utils/')
from item import Item
from currency import get_currency

NAME_LEN = 25

class User:

    def __init__(self, user_id, name=''):
        self.id = user_id
        self.user_name = name

        # Item objects

        self.item_list = []

    def add_item(self, url, name=None, proxies={}):
        item = Item(url)
        item.extract_info(proxies=proxies) # fetch soup and then name, price etc..

        if item.price == 0:
            return None

        if name: # User has provided custom name
            item.name = name

        created = db.ItemDb.get_or_none(db.ItemDb.owner == self.id,
                                db.ItemDb.url == url)

        if created: # Item is already added
            return False

        item = db.ItemDb.create(owner=self.id,
                                name=item.name,
                                price=int(item.price),
                                url=item.url)


        custom_item = Item(item.url, item.name, item.price)
        self.item_list.append(custom_item)
        return True

    def items_to_string(self, item_list):
        result = []
        for i in range(len(item_list)):
            item = item_list[i]
            # Sending text with Markdown support
            currency = get_currency(item.site_name)
            result.append(str(i+1) + "-) " + "["
                          + item.name[:NAME_LEN] + "]"
                          + "(" + item.url + ")"
                          + ": "+ currency + str(item.price)
                          + "\n")
        return result

    def check_prices(self):
        updated_items = []
        for item in self.item_list:
            old_price = item.price
            item.reset_info()
            item.update()
            if int(old_price) != int(item.price):
                # Sending text with Markdown support
                updated_items.append( "[" + item.name[:NAME_LEN] + "]"
                                     +"(" + item.url + ") \n"
                                     + str(old_price) + " --> "
                                     + str(item.price) + "\n")
                db_item = db.ItemDb.get(db.ItemDb.url==item.url)
                db_item.price = item.price
                db_item.save()

        message = ""
        if updated_items:
            message = "Hi " + self.user_name + " there is a price change\n"

        return "".join([message] + updated_items)

    def get_item_list(self):

        if len(self.item_list) == 0:
            self.get_items_from_database()

        for item in self.item_list:
            item.update()

        result = self.items_to_string(self.item_list)

        if len(result) == 0:
            return "You have not added any item, type /add url"

        return "".join(result)

    def get_items_from_database(self):
        """ Get items from database and save in self.item_list
        """
        item_list = db.get_user_items(self.id)

        for item in item_list:
            custom_item = Item(item.url, item.name, item.price)
            self.item_list.append(custom_item)

        return self.item_list

    def remove_item(self, item_no):
        item_list =  db.get_user_items(self.id)
        i=1
        for item in item_list: # Since item_list is fucking ModelSelect object
            # I cannot call range(item_list) FUCK IT FUCK FUCK FUCK
            if i == item_no:
                try:
                    if item.delete_instance():
                        del self.item_list[i-1]
                        return "Deleted the item succesfully"
                except Exception as e:
                    print(e)
                    return "Some error happened, uuppss"
            i += 1

        return "Please provide valid item number"
