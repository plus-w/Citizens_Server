import sqlite3

conn = sqlite3.connect('citizens.db')

c = conn.cursor()
c.execute('''CREATE TABLE NEWS
       (ID CHAR(32) PRIMARY KEY     NOT NULL,
       TITLE           TEXT    NOT NULL,
       URL            TEXT     NOT NULL,
       M_URL          TEXT     NOT NULL,
       IMG_URL        TEXT     NOT NULL,
       DATE        CHAR(10)    NOT NULL);''')
conn.commit()
conn.close()