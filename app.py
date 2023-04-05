import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():  # put application's code here
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():  # put application's code here
    return render_template('register.html')


@app.route('/judge/judge_a_poster', methods=('GET', 'POST'))
def judge_poster():  # put application's code here
    return render_template('judge_a_poster.html')


@app.route('/judge/posters_to_judge', methods=('GET', 'POST'))
def judge_poster_list():  # put application's code here
    return render_template('posters.html')


@app.route('/contestant/upload_poster', methods=('GET', 'POST'))
def contestant_upload():  # put application's code here
    return render_template('upload_poster.html')


@app.route('/contestant/view_poster', methods=('GET', 'POST'))
def contestant_view():  # put application's code here
    return render_template('view_poster.html')


if __name__ == '__main__':
    app.run()
