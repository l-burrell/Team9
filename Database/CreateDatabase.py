import sqlite3
from sqlite3 import Error

#Method to create connection with database
def create_database():
    conn = None

    try:
        #Create connection and print version
        conn = sqlite3.connect("PosterDatabase.db")
        print(sqlite3.version)

        #Creates tables
        cur = conn.cursor()

        #Posters (poster_id, poster_title, poster_emails, poster_category, poster_description, poster_image)
        posterQuery = "CREATE TABLE IF NOT EXISTS posters(poster_id INTEGER PRIMARY KEY AUTOINCREMENT, poster_title STRING NOT NULL, poster_emails STRING NOT NULL, poster_category STRING NOT NULL, poster_description STRING, poster_image BLOB);"
        cur.execute(posterQuery)

        #Scores (score_id, clarity, organization, content, relevance, visual appeal)
        scoreQuery = "CREATE TABLE IF NOT EXISTS scores(poster_id INTEGER PRIMARY KEY, clarity INT, organization INT, content INT, relevance INT, visuals INT);"
        cur.execute(scoreQuery)

        users = "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING NOT NULL, email STRING NOT NULL, password STRING NOT NULL, poster_id INTEGER);"
        cur.execute(users)

        #Insert data into db
        #insertQuery = "INSERT INTO posters (poster_title, poster_emails, poster_category, poster_description, poster_image) values ('Test Poster', 'asiegel11@student.gsu.edu', 'Undergraduate', 'This is a test poster designed to demonstrate our project. This poster information is read from our database using flask and python', null);"
        #cur.execute(insertQuery)
        #conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_database()
