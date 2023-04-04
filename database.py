import sqlite3

from users import Users

db_connection = sqlite3.connect(':memory:')

c = db_connection.cursor()

c.execute("""CREATE TABLE user_collection (
        name text,
        email text,
        password text
        )""")

c.execute("""CREATE TABLE poster_collection (
        title text,
        members text,
        category text,
        description text,
        id integer
        )""")
