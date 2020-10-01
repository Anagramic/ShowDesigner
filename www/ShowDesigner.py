from flask import Flask, render_template
from jinja2 import Template
app = Flask(__name__)

@app.route('/')
def index():
    answer = 4 + 6
    
    return render_template('index.html',answer=answer)

#@app.route('/microphone/<number>')
#def microphone(number):
#    return render_template('number.html',number=number)