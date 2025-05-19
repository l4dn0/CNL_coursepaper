import os
from pathlib import Path
import sqlite3


cnl = open('cnl_to_insert.txt', encoding="utf-8").readlines() # в этом файле будут лежать фразы в спецификации CNL
screensfolder = 'screens'  # тут нужно указать папку, в которой лежат скрины
fileslist = os.listdir(screensfolder)

try:
    f = open('images.db', 'x')

    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE writes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnl TEXT NOT NULL,
    raw BLOB);''')
    conn.commit()

    for i in range(len(fileslist)):
        if fileslist[i].endswith(('jpg', 'png', 'jpeg')):
            cursor.execute("INSERT INTO writes (cnl, raw) VALUES (?, ?);", [cnl[i], Path(screensfolder + '/' +
                                                                                      fileslist[i]).read_bytes()])

    conn.commit()
    cursor.close()
    conn.close()
except FileExistsError:
    print("Файл images.db уже существует.")