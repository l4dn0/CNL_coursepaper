import sqlite3
from sqlite3 import DatabaseError

try:
    _connection = sqlite3.connect('images.db')
    cursor = _connection.cursor()
except DatabaseError:
    print("Непредвиденная ошибка")


def select_all():
    cursor.execute('SELECT * FROM writes')
    return cursor.fetchall()
