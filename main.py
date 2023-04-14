from flask import Flask, render_template, request, flash, redirect, url_for, abort
import sqlite3

app = Flask(__name__)

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
                # return redirect(url_for('posters', posterID=account['poster_id']))



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
    all_posters = conn.execute('SELECT * FROM posters').fetchall()
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
        print('creating a new score for poster with id:', posterID)
        # create the scoring
        clarity = request.form['clarity']
        organization = request.form['organization']
        content = request.form['content']
        relevance = request.form['relevance']
        visuals = request.form['visuals']

        # TODO:
        # insert the scoring into the database, and connect to the posters table....

        return redirect(url_for('posters'))
    


# CONTESTANT ROUTES
@app.route('/contestant/upload_poster', methods=('GET', 'POST'))
def upload_poster():
    userID = request.args['userID']
    posterID = int(request.args['posterID'])
    # user = conn.execute('SELECT * FROM users WHERE user_id = ?', (userID,)).fetchone()

    print('poster:', posterID, ' user:', userID)
    
    if posterID == -1:
        print('This user did not have a poster -> creating the poster.')
        # create the poster
        # poster_title = request.form['title']
        # poster_emails = request.form['group_members']
        # poster_category = request.form['category']
        # poster_description = request.form['description']
        # poster_image = request.form['image']

        # testing data 
        poster_title = 'test title'
        poster_emails = 'mem1, mem2, mem3'
        poster_category = 'test category'
        poster_description = 'test description'
        poster_image = 'test image'
        

        conn = poster_db()

        conn.execute("""INSERT INTO posters (poster_title, poster_emails, poster_category, poster_description, poster_image) VALUES (?, ?, ?, ?, ?)""",
                     (poster_title, poster_emails, poster_category, poster_description, poster_image))
        print('successfully made poster')


        poster = conn.execute('SELECT * FROM posters WHERE poster_title = ?', (poster_title,)).fetchone()
        print('successfully found the poster')


        conn.execute('UPDATE users SET poster_id = ? WHERE user_id = ?', (poster['poster_id'], userID))
        # conn.execute('UPDATE users SET poster_id = ? WHERE user_id = ?', (posterID['poster_id'], userID))
        print('successfully updated the user with poster id ')

        # conn.execute("""UPDATE users SET poster_id = ? WHERE user_id = ?""", (poster['poster_id'], user['user_id']))
        # conn.execute("""UPDATE users SET (email, name, password, poster_id) VALUES (?, ?, ?, ?)""", 
        #                   (email, name, password, poster['poster_id']))
        # conn.commit()
        # conn.close()
        # return redirect(url_for('view_poster', posterID=poster['poster_id']))
        print("created the poster successfully")
        conn.close()

    else:
        print("we found the poster -> loading the poster")

    # return render_template('index.html')
    return redirect(url_for('index'))



@app.route('/contestant/view_poster', methods=('GET', 'POST'))
def contestant_view(posterID):  
    conn = poster_db()
    poster = conn.execute('SELECT * FROM posters WHERE poster_id = ?', (posterID,)).fetchall()
    conn.close()
    return render_template('view_poster.html', poster=poster)



# IN-PROGRESS
@app.route('//submit_poster', methods=['POST'])
def submit_poster():
    file = request.files['image']
    file.save('/path/to/save/folder/' + file.filename)
    return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run(debug=True)

