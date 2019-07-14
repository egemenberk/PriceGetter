import database as db
from user import User

class Server:

    def __init__(self):
        self.users = {}  # id, User

    def get_or_create_user(self, user_id, name):
        user, created = db.UserDb.get_or_create(id=user_id, name=name)
        custom_user = User(user_id, user.name)
        self.users[user_id] = custom_user
        custom_user.get_items()

    def ask_name(self, message):
        name = message.text

    def is_registered(self, user_id):
        try:
            self.users[user_id]
        except KeyError:
            return False
        return True

    def get_user(self, user_id):
        if self.is_registered(user_id):
            return self.users[user_id]
        else:
            user = db.get_user(user_id)
            if user:
                custom_user = User(user_id, user.name)
                self.users[user_id] = custom_user
                custom_user.get_items_from_database()
                return custom_user
            return None


