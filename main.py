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
            flash('ISSUE: not enough characters in text field...')
            return redirect(url_for('index'))
        conn = poster_db()
        account = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                     (email, password)).fetchone()
        conn.close()
        print('[account] user_id:', account['user_ID'], ' poster_id:',account['poster_ID'])

        if account == None:
            flash('Incorrect login credentials')
            return render_template('index.html')
        else:
            if "@student.gsu.edu" in email:
                return redirect(url_for('upload_poster', userID=account['user_id'], posterID=account['poster_id']))
            else:
                return redirect(url_for('posters', posterID=account['poster_id']))



@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        if len(name) < 1 or len(email) < 1 or len(password) < 1:
            flash('ISSUE: not enough characters in text field...')
            return redirect(url_for('register'))
        if password == confirmPassword:
            conn = poster_db()
            account = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if account == None:
                print('OK: creating the account')
                conn.execute("""INSERT INTO users (email, name, password) VALUES (?, ?, ?)""", 
                          (email, name, password))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))
            else:
                conn.close()
                flash('ISSUE: account already found in the database...')
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
    # conn = poster_db()
    print('found it:', posterID)
    return render_template('judge_poster.html')



# CONTESTANT ROUTES
@app.route('/contestant/upload_poster', methods=('GET', 'POST'))
def upload_poster(userID, posterID):
    conn = poster_db()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (userID,)).fetchone()
    
    print(user, " HERE IT IS HERE IT IS")

    if user is None:
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

        print('poster:', posterID, ' user:', userID)

        # create the poster
        # conn.execute("""INSERT INTO posters (poster_title, poster_emails, poster_category, poster_description, poster_image) VALUES (?, ?, ?, ?, ?)""",
                    #  (poster_title, poster_emails, poster_category, poster_description, poster_image))
        conn.close()
        
        # get the poster id
        # new_poster
        # poster = conn.execute('SELECT * FROM posters WHERE poster_id = ?', (posterID,)).fetchone()

        # conn.execute("""UPDATE users SET poster_id = ? WHERE user_id = ?""", (new_poster['poster_id'], user['user_id']))
        # conn.execute("""UPDATE users SET (email, name, password, poster_id) VALUES (?, ?, ?, ?)""", 
        #                   (email, name, password, poster['poster_id']))



        # conn.execute("""INSERT INTO users (email, name, password) VALUES (?, ?, ?)""", 
        #             (email, name, password))
        # conn.commit()
        # conn.close()
        # return redirect(url_for('view_poster', posterID=poster['poster_id']))
    else:
        print("this user did have a poster -> loading the poster")
    return render_template('index.html')



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

