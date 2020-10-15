from flask import Flask, render_template
from jinja2 import Template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/microphone/<number>')
#def microphone(number):
#    return render_template('number.html',number=number)