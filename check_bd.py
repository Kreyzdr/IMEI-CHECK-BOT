import sqlite3
from sekret.key import DATABASE # Имя базы данных


# Подключаемся к базе данных
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# Проверяем список таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе данных:")
for table in tables:
    print(table[0])


# Проверяем содержимое таблицы whitelist
cursor.execute("SELECT * FROM whitelist;")
whitelist = cursor.fetchall()
print("\nСодержимое таблицы whitelist:")
for row in whitelist:
    print(row)


# Проверяем содержимое таблицы tokens
cursor.execute("SELECT * FROM tokens;")
tokens = cursor.fetchall()
print("\nСодержимое таблицы tokens:")
for row in tokens:
    print(row)



conn.close()