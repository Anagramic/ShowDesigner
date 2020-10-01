from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    answer = 4 + 6
    return f'<h1>Answer is {answer}</h1>'

@app.route('/microphone/<number>')
def microphone(number):
    return f'<h1>This is microphone {number}</h1>'