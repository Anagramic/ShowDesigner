from flask import Flask, render_template
from jinja2 import Template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#finds the directory this file file is stored under
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] =\
    "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SSQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/microphone/<number>')
#def microphone(number):
#    return render_template('number.html',number=number)

# Models
class InputDevice(db.Model):
    __tablename__ = "InputDevice"
    id = db.Column(db.Integer, primary_key=True)
    Manufacturer = db.Column(db.String(64))
    Model = db.Column(db.String(64))
    Type = db.Column(db.String(64))

class OutputDevice(db.Model):
    __tablename__ = "OutputDevice"
    id = db.Column(db.Integer, primary_key=True)
    Manufacturer = db.Column(db.String(64))
    Model = db.Column(db.String(64))
    Type = db.Column(db.String(64))

class StageBox(db.Model):
    __tablename__ = "StageBox"
    id = db.Column(db.Integer, primary_key=True)
    Inputs = db.Column(db.Integer)
    Outputs = db.Column(db.Integer)

class Show(db.Model):
    __tablename__ = "Show"
    id = db.Column(db.Integer, primary_key=True)
    ShowName = db.Column(db.String(64))

class ShowStageBox(db.Model):
    __tablename__ = "ShowStageBox"
    id = db.Column(db.Integer, primary_key=True)
    ShowID = db.Column(db.Integer)
    StageBoxID = db.Column(db.Integer)

class InputMapping(db.Model):
    __tablename__ = "InputMapping"
    id = db.Column(db.Integer, primary_key=True)
    ShowStageBoxID = db.Column(db.Integer)
    Port = db.Column(db.Integer)
    InputID = db.Column(db.Integer)
    StripPosition = db.Column(db.Integer)
    Label = db.Column(db.String(64))