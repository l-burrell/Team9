from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')


@app.route('/register')

def register():
    return render_template('register.html')


@app.route('/PostersToJudge')

def PostersToJudge():
    return render_template('PostersToJudge.html')


@app.route('/upload_poster')
def Upload_poster():
    return render_template('Upload_poster.html')


@app.route('/submit_poster', methods=['POST'])
def submit_poster():
    file = request.files['image']
    file.save('/path/to/save/folder/' + file.filename)
    # do something with the file
    return 'File uploaded successfully!'


if __name__ == '__main__':
    app.run(debug=True)

