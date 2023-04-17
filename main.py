from flask import Flask, render_template, request, flash, redirect, url_for, abort, Blueprint, send_from_directory
import sqlite3
import os

#Import Database files
from Database import PosterDriver
from Database.PosterDriver import PosterRetriever
from Routing.ViewPoster_Routing import ViewPoster_Routing

from werkzeug.utils import secure_filename

#insecting the image library 
from PIL import Image
import io

#Create Database; Comment out if not needed
#from Database import CreateDatabase
#CreateDatabase.create_database()

#Create app and register blueprint
app = Flask(__name__)
app.register_blueprint(ViewPoster_Routing)

app.config['SECRET_KEY'] = "thiswasoursecretkeyokay"
app.config['UPLOAD_FOLDER'] = "./static/images"
    

# connect to the database
def poster_db():
    conn = sqlite3.connect('PosterDatabase.db')
    conn.row_factory = sqlite3.Row
    return conn


# # GENERAL ROUTES
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:
        email = request.form['email']
        password = request.form['password']
        if len(email) < 1 or len(password) < 1:
            flash('ISSUE: not enough characters in text field.')
            return redirect(url_for('index'))
        conn = poster_db()
        if not conn:
            return render_template('index.html')
        cur = conn.cursor()
        account = cur.execute('SELECT user_id, poster_id FROM users WHERE email = ? AND password = ?',
                     (email, password)).fetchone()
        conn.close()
        if account == None:
            flash('ISSUE: Incorrect login credentials')
            return render_template('index.html')
        else:
            if "@student.gsu.edu" in email:
                print("FOUND: user:", account['user_id'], ' poster: ', account['poster_id'])
                return redirect(url_for('upload_poster', userID=account['user_id'], posterID=account['poster_id']))
            else:
                return redirect(url_for('posters'))




@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        poster_id = -1
        if len(name) < 1 or len(email) < 1 or len(password) < 1:
            flash('ISSUE: not enough characters in text field.')
            return redirect(url_for('register'))
        if password == confirmPassword:
            conn = poster_db()
            if not conn:
                return redirect(url_for('register'))
            cur = conn.cursor()
            account = cur.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if account == None:
                print('OK: creating the account')
                cur.execute("""INSERT INTO users (email, name, password, poster_id) VALUES (?, ?, ?, ?)""", 
                          (email, name, password, poster_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            else:
                conn.close()
                flash('ISSUE: account already found in the database.')
                return render_template('register.html')




# JUDGE ROUTES
@app.route('/judge/posters', methods=('GET', 'POST'))
def posters():
    conn = poster_db()
    is_rated = 'false'
    if conn:
        cur = conn.cursor()
        all_posters = cur.execute('SELECT * FROM posters WHERE is_rated = ?', (is_rated,)).fetchall()
        conn.close()
        return render_template('posters.html', all_posters=all_posters, count=len(all_posters))
    return render_template('poster.html', all_posters=None, count=0)




@app.route('/judge/posters/<posterID>', methods=('GET', 'POST'))
def rate_poster(posterID):
    if request.method == 'GET':
        conn = poster_db()
        poster = conn.execute('SELECT * FROM posters WHERE poster_id = ?', (posterID,)).fetchone()
        conn.close()
        print('displaying poster with id:', posterID)
        return render_template('judge_poster.html', poster=poster)
    else:
        conn = poster_db()
        clarity = request.form['clarity']
        organization = request.form['organization']
        content = request.form['content']
        relevance = request.form['relevance']
        visuals = request.form['visuals']
        is_rated = 'true'
        if conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO scores (poster_id, clarity, organization, content, relevance, visuals) VALUES (?, ?, ?, ?, ?, ?)""",
                        (posterID, clarity, organization, content, relevance, visuals))
            conn.commit()
            cur.execute('UPDATE posters SET is_rated = ? WHERE poster_id = ?', (is_rated, posterID,))
            conn.commit()
        return redirect(url_for('posters'))




# CONTESTANT ROUTES
@app.route('/upload_poster', methods=(['GET','POST']))
def upload_poster():
    userID = request.args.get("userID")
    if request.args.get("posterID"):
        posterID = int(request.args.get("posterID"))
    else:
        posterID = -1
    print('poster:', posterID, ' user:', userID)
    if request.method == "GET":    
        if posterID != -1:
            return redirect(url_for('ViewPoster_Routing.view_poster', poster_id=posterID))
        return render_template("upload_poster.html", userID=userID)
    else:
        #User does not have a poster
        poster_title = request.form['title']
        poster_emails = request.form['group_email']
        poster_category = request.form['category']
        poster_description = request.form['description']
        if len(poster_title) < 1:
            flash("ISSUE: Please enter a poster title")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        if len(poster_emails) < 1:
            flash("ISSUE: Please enter a poster email")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        if len(poster_category) < 1:
            flash("ISSUE: Please enter a poster category")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))   
        if len(poster_description) < 1:
            flash("ISSUE: Please enter a poster description")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        poster_image = request.files['file']
        if poster_image.filename == '':
            flash("ISSUE: Please submit an image")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        if not poster_image:
            flash("ISSUE: Could not upload poster")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        if not allowed_file(poster_image.filename):
            flash("ISSUE: Please submit a .jpg or .png file")
            return redirect(url_for('upload_poster', userID=userID, posterID=posterID))
        filename = secure_filename(poster_image.filename)
        # filename = secure_filename(posterID + '.' +filename.rsplit('.', 1)[1])
        poster_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = poster_db()
        if conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO posters (poster_title, poster_emails, poster_category, poster_description, poster_image) VALUES (?, ?, ?, ?, ?)""",
                        (poster_title, poster_emails, poster_category, poster_description, filename))
            poster = cur.execute('SELECT last_insert_rowid()').fetchone()
            conn.commit()
            if poster:
                userID = request.args.get("userID")
                print("userID: " + userID)
                print(poster[0])
                cur.execute('UPDATE users SET poster_id = ? WHERE user_id = ?', (poster[0], userID))
                conn.commit()
            return redirect(url_for('ViewPoster_Routing.view_poster', poster_id=poster[0]))
        return render_template("upload_poster.html", userID=userID)




def allowed_file(filename):
    return filename.lower().endswith((".png", ".jpg"))



@app.route('/uploads/<file>')
def import_image(file):
    userID = request.args.get("userID")
    posterID = request.args.get("posterID")
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)



#inserting the image into the database
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    # Read the image data and convert it to bytes
    img = Image.open(io.BytesIO(file.read()))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    # Save the image bytes to the database
    conn = poster_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO images (filename, data) VALUES (?, ?)', (filename, img_bytes))
    conn.commit()
    conn.close()




@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='images/'+filename), code=301)




if __name__ == '__main__':
    app.run(debug=True)

