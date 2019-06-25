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

def print_items():
    for item in ItemDb.select():
        if item.category == "islemciler":
            print(item.name[:30], "\t", item.price, "\t",item.category, "\t",item.fetch_time)
    #print(len(ItemDb.select()))

if __name__ == '__main__':
    print_items()
