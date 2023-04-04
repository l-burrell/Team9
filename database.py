import sqlite3
from users import User

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


def create_user(account):
    with db_connection:
        c.execute("""INSERT INTO user_collection VALUES
        (:name, :email, :password)""", 
        {'name':account.name, 'email':account.email, 'password':account.password})


def get_user(email):
    with db_connection:
        c.execute("""SELECT * FROM user_collection WHERE email=:email""", {'email':email})
        return c.fetchone()


def create_poster(poster):
    with db_connection:
        c.execute("""INSERT INTO poster_collection VALUES(:title, :members, :category, :description, :id)""", 
                  {"title":poster.title, "members":poster.members, "category":poster.category, "description":poster.description, "id":poster.id})


def get_poster(id):
    with db_connection:
        c.execute("""SELECT * FROM poster_collection WHERE id=:id""", {'id':id})
        return c.fetchone()


def update_poster(poster):
    with db_connection:
        c.execute("""UPDATE poster_collection SET title=:title, members=:members, category=:category, description=:description WHERE id=:id""", 
              {'title':poster.title, 'members':poster.members, 'category':poster.category, 'description':poster.description})
    

def delete_poster(poster):
    with db_connection:
        c.execute("""DELETE from poster_collection WHERE id=:id""", 
                  {'poster_id':poster.poster_id})


acc = User('John', 'so@student.gsu.edu', 'password')

create_user(acc)

print("\n [user-db]:", get_user(acc.email))

acc.create_poster('The Toaster', "bob,tim,james", 'AI', 'the color is rainbow technicolor')

create_poster(acc.poster)

print("\n [poster db]:", get_poster(acc.poster.id))

print("\n")
db_connection.close()

