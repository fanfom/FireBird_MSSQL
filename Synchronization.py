import fdb
import os
import datetime
import sys
import logging
import pyodbc

filelist = os.listdir(path=".")
logger = logging.getLogger("SynchLog")
# По красоте это через logging сделать конечно но так хоть и говнокод но работать будет, на малых дистанциях можно схалтурить чутка ;)
# ну или если мы хотим что б проверка шла до обращения к базе
# if "firstname.txt" in filelist:
#     open("log.txt","a").write(str(datetime.datetime.now())+"    Файл firstname.txt существует, скрипт остановлен")
#     print("Файл firstname.txt существует, скрипт остановлен")
#     sys.exit()
# if "surname.txt" in filelist:
#     open("log.txt","a").write(str(datetime.datetime.now())+"    Файл surname.txt существует, скрипт остановлен")_
#     print("Файл surname.txt существует, скрипт остановлен")
#     sys.exit()

# Ясен красен никто не будет в скрипте под мастер паролем(тем более стандартным подключатся,
# для этого нужны спец учетки со спец правами, но задание про скрипты вроде так что лан)
con = fdb.connect(dsn="D:\\FireBird\\CLIENTS.FBD", user='SYSDBA', password='masterkey')

sur = con.cursor()
sur.execute("select * from surname;")
first = con.cursor()
first.execute("select * from firstname;")
try:
#было лениво переписывать эту часть поскольку fetchal обнуляет свою переменную, а я дальше на нее ссылаюсь, сожрал немного памяти
    t = sur
    open("surname.txt", "x").write(str(t.fetchall()))
    t = first
    open("firstname.txt", "x").write(str(t.fetchall()))
    cnx = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                         "Server=FANFOM-LAPTOP\\SQLEXPRESS;"
                         "Database=Clients;"
                         "uid=aaa;pwd=15320")
    Cursor = cnx.cursor()
    for data in (sur.fetchall()):
        id = str(data[0])
        firstname = first.fetchone()[1]
        surname = data[1]
        sql = f"INSERT INTO NAMES  VALUES ({id},'{firstname}','{surname}')"
        Cursor.execute(sql)
except Exception as msg:
    print(msg)
    open("log.txt", "a").write(str(datetime.datetime.now()) + str(msg) + "\n")
    sys.exit()
