import sqlite3
from sqlite3 import Error

#Method to create connection with database
def create_connection():
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

        #Insert data into db
        #insertQuery = "INSERT INTO posters(poster_title, poster_emails, poster_category, poster_description, poster_image) VALUES ('Test', 'asiegel11@student.gsu.edu', 'Undergraduate', 'This is a test poster not meant to do anything', NULL);"
        #cur.execute(insertQuery)
        #conn.commit()


    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

