import MySQLdb
from passwd import *

# Функция для печати таблицы
def print_table(cur):
    data=cur.fetchall()
    for key in data:
        print(key,end='\n')

# Функция для подключения
def connect():
    try:
        database = MySQLdb.connect(host='localhost', user='root', passwd=get_passwd(), db='product')
        return database
    except MySQLdb.Error as error:
        print('Connecting error {}'.format(error))
        database.close()

# Функция добавления строки в таблицу и вывода таблицы
def add_and_print(database):
    try:
        # Создаём новый объект(курсор)
        cur = database.cursor(MySQLdb.cursors.DictCursor)
        # Кортеж с вводимыми данными
        cort = ('Afdgdsdgdsff', 'dfsgdfgdfgdfgdfsdfg', 19, 1, 'Applied Mathematics', 'sftetdfgdfetwe345f@mail.ru')
        # Даём курсору команду выполнить запрос
        cur.execute('INSERT INTO Hmmm(FirstName,LastName,Age,Course,Direction,Email) '
        'VALUES (%s,%s,%s,%s,%s,%s)',cort)
        # Сохраняем изменения
        database.commit()
        # Даём курсору команду выполнить запрос
        cur.execute('SELECT * FROM Hmmm')
        print_table(cur)
        сur.close()
    except MySQLdb.Error as error:
        print('Query error: {}'.format(error))
        database.close()

if __name__ == '__main__':
    database = connect()
    add_and_print(database)
    database.close()

