from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('poster.html')

@app.route('/submit_poster', methods=['POST'])
def submit_poster():
    file = request.files['image']
    file.save('/path/to/save/folder/' + file.filename)
    # do something with the file
    return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(debug=True)
