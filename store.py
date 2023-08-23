import sqlite3
import time
import math


class StoreDB:
    def __init__(self, db):

        self.__db = db
        self.__cur = db.cursor()


    def add_user(self, firstname, lastname,  hpsw, email):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                err = f"Пользователь с таким email уже существует"
                print(err)
                return False, err

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users(firstname, lastname, password, email)  VALUES(?, ?, ?, ?)",
                               (firstname, lastname, hpsw, email))
            self.__db.commit()
        except sqlite3.Error as e:
            err = f"Ошибка добавления пользователя в БД " + str(e)
            print(err)
            return False, err

        return True, None

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def del_user(self, user_id):
        try:
            self.__cur.execute(f"DELETE FROM users WHERE id = {user_id}")
            self.__db.commit()

            return True
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False
