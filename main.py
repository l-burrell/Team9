from flask import Flask, render_template, request, flash, redirect, url_for, abort, Blueprint
import sqlite3

#Import Database files
from Database import PosterDriver
from Database.PosterDriver import PosterRetriever

#Create routing blueprint
from Routing.ViewPoster_Routing import ViewPoster_Routing

app = Flask(__name__)
app.register_blueprint(ViewPoster_Routing)

app.config['SECRET_KEY'] = "thiswasoursecretkeyokay"
    

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
        account = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
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
            account = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if account == None:
                print('OK: creating the account')
                conn.execute("""INSERT INTO users (email, name, password, poster_id) VALUES (?, ?, ?, ?)""", 
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
    all_posters = conn.execute('SELECT * FROM posters WHERE is_rated = ?', (is_rated,)).fetchall()
    conn.close()
    return render_template('posters.html', all_posters=all_posters, count=len(all_posters))




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
        conn.execute("""INSERT INTO scores (poster_id, clarity, organization, content, relevance, visuals) VALUES (?, ?, ?, ?, ?, ?)""",
                    (posterID, clarity, organization, content, relevance, visuals))
        conn.commit()
        conn.execute('UPDATE posters SET is_rated = ? WHERE poster_id = ?', (is_rated, posterID,))
        conn.commit()
        return redirect(url_for('posters'))
    


# CONTESTANT ROUTES
@app.route('/contestant/upload_poster', methods=('GET', 'POST'))
def upload_poster():
    userID = request.args['userID']
    posterID = int(request.args['posterID'])
    print('poster:', posterID, ' user:', userID)
    if request.method == 'GET':
        if posterID == -1:
            return render_template('upload_poster.html')
        else:
            return redirect(url_for('view_poster', posterID=posterID))
    else:
        poster_title = request.form['title']
        poster_emails = request.form['group_members']
        poster_category = request.form['category']
        poster_description = request.form['description']
        poster_image = request.form['image']
        is_rated = 'false'
        conn = poster_db()
        conn.execute("""INSERT INTO posters (poster_title, poster_emails, poster_category, poster_description, poster_image, is_rated) VALUES (?, ?, ?, ?, ?, ?)""",
                    (poster_title, poster_emails, poster_category, poster_description, poster_image, is_rated))
        conn.commit()
        poster = conn.execute('SELECT * FROM posters WHERE poster_title = ?', (poster_title,)).fetchone()
        conn.commit()
        conn.execute('UPDATE users SET poster_id = ? WHERE user_id = ?', (poster['poster_id'], userID))
        conn.commit()
        conn.close()

    # return redirect(url_for('index'))



@app.route('/contestant/view_poster/<posterID>', methods=('GET', 'POST'))
def view_poster(posterID):  
    conn = poster_db()
    poster = conn.execute('SELECT * FROM posters WHERE poster_id = ?', (posterID,)).fetchone()
    conn.commit()
    score = conn.execute('SELECT * FROM scores WHERE poster_id = ?', (posterID,)).fetchone()
    conn.commit()
    conn.close()
    return render_template('view_poster.html', poster=poster, score=score)



# IN-PROGRESS
@app.route('//submit_poster', methods=['POST'])
def submit_poster():
    file = request.files['image']
    file.save('/path/to/save/folder/' + file.filename)
    return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run(debug=True)

