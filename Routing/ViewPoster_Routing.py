#Import flask
from flask import Flask, Blueprint, render_template

#Create routing blueprint
ViewPoster_Routing = Blueprint('ViewPoster_Routing', __name__)

#Route poster page based off poster_id in url
@ViewPoster_Routing.route('/View_Poster/<string:poster_id>')
def load_poster(poster_id):
   return render_template('View_Poster.html', id=poster_id)



