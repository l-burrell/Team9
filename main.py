from flask import Flask, render_template, request

app = Flask(__name__)


# GENERAL ROUTES
@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    return render_template('register.html')



# JUDGE ROUTES
@app.route('/judge/posters', methods=('GET', 'POST'))
def posters():
    return render_template('posters.html')


@app.route('/judge/rate', methods=('GET', 'POST'))
def rate():
    return render_template('judge_poster.html')



# CONTESTANT ROUTES
@app.route('/contestant/upload_poster', methods=('GET', 'POST'))
def upload_poster():
    return render_template('upload_poster.html')


@app.route('/contestant/view_poster', methods=('GET', 'POST'))
def contestant_view():  
    return render_template('view_poster.html')



# IN-PROGRESS
@app.route('//submit_poster', methods=['POST'])
def submit_poster():
    file = request.files['image']
    file.save('/path/to/save/folder/' + file.filename)
    return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run(debug=True)

