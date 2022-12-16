import sqlite3

conn = sqlite3.connect("./instance/db_antrian.db")
curs = conn.cursor()
curs.execute('SELECT * FROM user')
cek = curs.fetchmany()
print(cek)