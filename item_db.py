#!/usr/bin/env python3
import argparse
from peewee import *
import datetime

db = SqliteDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class ItemDb(BaseModel):
    url = CharField()
    name = CharField()
    price = IntegerField()
    category = CharField(null=True, default=None)
    fetch_time = DateTimeField(default=datetime.datetime.now())

db.create_tables([ItemDb])

def print_item(item):
    print(item.name[:30], "\t", "₺" + str(item.price), "\t",item.category, "\t",item.fetch_time)

def search_item(name):
    for item in ItemDb.select():
        if name.upper() in item.name.upper():
            print_item(item)

def print_all_items():
    for item in ItemDb.select():
        print(item.name[:30], "\t", "₺" + str(item.price), "\t",item.category)

def print_items_time(category):
    for item in ItemDb.select():
        #if category in item.category:
        diff = datetime.datetime.now() - item.fetch_time
        if (diff.seconds / 60 / 60) < 1:
            print(item.name[:30], "\t", "₺" + str(item.price), "\t",item.category, "\t",item.fetch_time)
    #print(len(ItemDb.select()))

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--category", help="Fetch the items from given category")
    parser.add_argument("-s", "--search", help="Search item with name")
    parser.add_argument("-a", "--all", help="Print all items")
    args = parser.parse_args()
    return args

# CAUTION
def delete(category):
    for item in ItemDb.select():
        if item.category == args.category:
            diff = datetime.datetime.now() - item.fetch_time
            if (diff.seconds / 60 / 60) < 1:
                print(item.name)
                #print(item.delete_instance())

if __name__ == '__main__':
    args = handle_args()
    if args.all:
        print_all_items()
    if args.category:
        print_items(args.category)
    if args.search:
        search_item(args.search)
