import database as db
from user import User

class Server:

    def __init__(self):
        self.users = {}  # id, User

    def create_user(self, user_id, name):
        """ This creates a new user if the user was not registered
        """
        if self.is_registered(user_id):
            return self.users[user_id]
        user, created = db.UserDb.get_or_create(id=user_id, name=name)
        self.users[user_id] = User(user_id, user.name)
        self.users[user_id].get_items_from_database()

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
            return None

    def start(self):
        """ It will be called whenever the server has started
        It will fetch all registerd users and their watchlists from the database
        """
        for db_user in db.UserDb.select():
            user = User(db_user.id, db_user.name)
            user.get_items_from_database()
            self.users[db_user.id] = user

