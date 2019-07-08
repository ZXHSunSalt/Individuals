from database.__init__ import *


class Database():
    def __init__(self, database_name):
        self.db = pymysql.connect("localhost", "root", "jhx123456", database_name)
        self.cursor = self.db.cursor()

    def _commit(self):
        self.db.commit()

    def _close(self):
        self.db.close()

    def _creat_database(self, name):
        sql = "create database" + name
        self.cursor.execute(sql)

    def _insert_data(self, sheet_name, keys, values):
        # for i in range(len(keys)):
        k_item = ",".join(keys)

        item = ""
        for v in values:
            v_item = "'" + v + "'"
            item = item + v_item + ","

        key = "(" + k_item + ")"
        value = "(" + item[:-1] + ")"
        sql = "INSERT INTO %s "%(sheet_name) + key + " VALUES " + value
        self.cursor.execute(sql)

    def _get_data(self, sheet_name):
        sql = "SELECT * FROM %s "%(sheet_name)
        self.cursor.execute(sql)
        all_data = self.cursor.fetchall()
        return all_data

if __name__ == "__main__":

    database = Database()

