#Import flask
from flask import Flask, Blueprint, render_template

from sqlite3 import Error

#Import Database files
from Database import PosterDriver
from Database.PosterDriver import PosterRetriever

#Create routing blueprint
ViewPoster_Routing = Blueprint('ViewPoster_Routing', __name__)

#Route poster page based off poster_id in url
@ViewPoster_Routing.route('/view_poster/<int:poster_id>')
def load_poster(poster_id):

   #Create instance of the class
   dbDriver = PosterRetriever(poster_id)

   #Load file using poster_id
   try:
      #Retrieve data from DataRetriever class
      poster_title = dbDriver.get_poster_title()
      poster_emails = dbDriver.get_poster_emails()
      poster_category = dbDriver.get_poster_category()
      poster_description = dbDriver.get_poster_description()
      scores = dbDriver.get_poster_scores()

      #Read each score
      clarity = scores[0]
      organization = scores[1]
      content = scores[2]
      relevance = scores[3]
      visual = scores[4]

   except Error as e:
      #Print error and set vars as error message
      print(e)
      poster_title = "Could not load title"
      poster_emails = "Could not load emails"
      poster_category = "Could not load category"
      poster_description = "Could not load description"
      clarity, organization, content, relevance, visual = "x"

   #Check if scores are integers or not before calculating total
   if isinstance(clarity, int):
      total = clarity + organization + content + relevance + visual
   else:
      total = "x"

   #Render data into html page
   return render_template('View_Poster.html', id=poster_id, title=poster_title, emails=poster_emails, category=poster_category, description=poster_description, clarity_rating=clarity, organization_rating=organization, content_rating=content, relevance_rating=relevance, visuals_rating=visual, total_rating=total)
