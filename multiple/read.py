import json
from collections import defaultdict
from hashlib import md5

import pymysql
from DBUtils.PooledDB import PooledDB
from openpyxl import load_workbook


CONN_CONFIG = {
    "host": "192.168.12.10",
    "port": 4002,
    "user": "root",
    "passwd": "iiecas",
    "db": "register",
    'charset': 'utf8',
}


class SQLPoll(object):

    # docstring for DbConnection

    __poll = None

    def __init__(self):
        self.pool = self.__get_db()
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    @classmethod
    def __get_db(cls):
        if cls.__poll is None:
            cls.__poll = PooledDB(
                creator=pymysql,
                mincached=10,
                maxconnections=100,
                **CONN_CONFIG)
        return cls.__poll

    def fetch_all(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def fetch_one(self, sql, args=None):
        if args is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def execute(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()
        result = self.cursor.lastrowid
        return result

    def __close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


path = "pass_word.xlsx"

workbook = load_workbook(path)

sheet = workbook["Sheet1"]

data = []

row_list = list(sheet.rows)[1:189]

for row in row_list:
	row_data = []
	cols = [row[index] for index in (0, 1, 2)]
	for cell in cols:
		row_data.append(cell.value)

	data.append(row_data)


query_one = '''
	SELECT
		login_id 
	FROM
		sys_login 
	WHERE
		username = %s
'''
sql_one = '''
	UPDATE register_accountpasswordchanged 
	SET `password` = %s
	WHERE
		login_id= %s
'''

with SQLPoll() as db:
	for item in data:
		username, secret, password = item
		if str(password) == '0':
			continue
		login_id = db.fetch_one(query_one, (username,))["login_id"]
		db.execute(sql_one, (password, login_id))

# print(data)
# result = []
# error = []
# for item in data:
# 	username, secret, password = item
# 	if str(password) != '0':
# 		if secret == md5(bytes(str(password), encoding='utf-8')).hexdigest():
# 			result.append(username)
# 		else:
# 			error.append(username)
# print(result)
# print(len(result))
# print(error)
# print(len(error))