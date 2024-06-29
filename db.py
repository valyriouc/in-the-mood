import sqlite3
import constants

conn = sqlite3.Connection(constants.DATABASE_NAME)

category_table_sql = '''CREATE TABLE category(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100) NOT NULL)'''

idea_table_sql = '''CREATE TABLE ideas(id INTEGER PRIMARY KEY AUTOINCREMENT, heading TEXT NOT NULL, content TEXT, fcategory INTEGER REFERENCES category(id))''' 
    

def init():
    is_init = False
    with open("constants.py", "r") as fobj:
        for line in fobj.readlines():
            if line.strip().startswith("DB_INIT"):
                is_init = True
                break
            
    if not is_init:
        with open("constants.py", "a") as fobj:
            fobj.write("\nDB_INIT=True")
        cur = conn.cursor().execute(category_table_sql)
        conn.cursor().execute(idea_table_sql)
        conn.commit()
