from flask_login import UserMixin


class User(UserMixin):
    def from_db(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def del_user(self, user_id, db):
        return db.del_user(user_id)

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def get_name(self):
        return f"{self.__user['lastname']} {self.__user['firstname']}" if self.__user else "User"

    def get_email(self):
        return self.__user['email'] if self.__user else str.empty

    def get_firstname(self):
        return self.__user['firstname'] if self.__user else ""

    def get_lastname(self):
        return self.__user['lastname'] if self.__user else ""

