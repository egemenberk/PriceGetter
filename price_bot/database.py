from peewee import *


db = SqliteDatabase("telegram.db")


class BaseModel(Model):
    class Meta:
        database = db


class UserDb(BaseModel):

    id = IntegerField(primary_key=True)
    name = CharField()


class ItemDb(BaseModel):

    id = AutoField()
    name = CharField()
    url = CharField()
    price = IntegerField()
    owner = ForeignKeyField(UserDb, backref="item_owner")

db.create_tables([UserDb, ItemDb])


def print_users():
    for user in UserDb.select():
        print(user.name, user.id)


def print_items():
    for item in ItemdDb.select():
        print(item.name[:25], item.owner)


def get_user_items(user_id):
    return ItemDb.select().where(UserDb.owner == user_id)

