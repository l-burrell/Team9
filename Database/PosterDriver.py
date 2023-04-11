#import SQLite
import sqlite3
from sqlite3 import Error

#Start of class
class PosterRetriever:

    #Class constructor
    def __init__(self, posterID):
        self.poster_id = posterID

    #Returns the title of the poster using poster_id
    def get_poster_title(self):

        #Create connection
        conn = sqlite3.connect("PosterDatabase.db")

        #Throw error if no connection established
        if conn is None:
            raise Exception("Could not connect to database")
        
        #Create cursor
        cur = conn.cursor()

        #Takes poster id and fetches the poster_title from database
        query = "SELECT poster_title FROM posters WHERE poster_id="+str(self.poster_id)
        result = cur.execute(query)
        title = cur.fetchone()

        #Close connection and return value
        conn.close()

        #Check if result is valid before subscripting
        if title is not None:
            return title[0]
        
        #Return invalid statement
        return "None"


    #Returns the emails of the poster using poster_id
    def get_poster_emails(self):

        #Create connection
        conn = sqlite3.connect("PosterDatabase.db")

        #Throw error if no connection established
        if conn is None:
            raise Exception("Could not connect to database")
        
        #Create cursor
        cur = conn.cursor()

        #Takes poster id and fetches the poster_title from database
        query = "SELECT poster_emails FROM posters WHERE poster_id="+str(self.poster_id)
        result = cur.execute(query)
        emails = cur.fetchone()

        #Close connection and return value
        conn.close()

        #Check if result is valid before subscripting
        if emails is not None:
            return emails[0]
        
        #Return invalid statement
        return "None"
    

    #Returns the description of the poster using poster_id
    def get_poster_description(self):

        #Create connection
        conn = sqlite3.connect("PosterDatabase.db")

        #Throw error if no connection established
        if conn is None:
            raise Exception("Could not connect to database")
        
        #Create cursor
        cur = conn.cursor()

        #Takes poster id and fetches the poster_title from database
        query = "SELECT poster_description FROM posters WHERE poster_id="+str(self.poster_id)
        result = cur.execute(query)
        description = cur.fetchone()

        #Close connection and return value
        conn.close()

        #Check if result is valid before subscripting
        if description is not None:
            return description[0]
        
        #Return invalid statement
        return "None"
    

    #Returns the category of the poster using poster_id
    def get_poster_category(self):

        #Create connection
        conn = sqlite3.connect("PosterDatabase.db")

        #Throw error if no connection established
        if conn is None:
            raise Exception("Could not connect to database")
        
        #Create cursor
        cur = conn.cursor()

        #Takes poster id and fetches the poster_title from database
        query = "SELECT poster_category FROM posters WHERE poster_id="+str(self.poster_id)
        result = cur.execute(query)
        category = cur.fetchone()

        #Close connection and return value
        conn.close()

        #Check if result is valid before subscripting
        if category is not None:
            return category[0]
        
        #Return invalid statement
        return "None"





