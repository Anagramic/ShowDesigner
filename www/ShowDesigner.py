from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    answer = 4 + 6
    return render_template('index.html')

@app.route('/microphone/<number>')
def microphone(number):
    return render_template('number.html',number=number)