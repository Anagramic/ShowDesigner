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

@app.route('/kit')
def kit():
    return render_template('kit.html')

@app.route('/shows')
def shows():
    shows = Show.query.all()
    return render_template('shows.html', shows=shows)

@app.route('/show/<showid>')
def show():
    return render_template('show.html')

@app.route('/design/<showid>')
def design():
    return render_template('design.html')

@app.route('/editkit')
def editkit():
    return render_template('editkit.html')







#@app.route('/microphone/<number>')
#def microphone(number):
#    return render_template('number.html',number=number)


#names on page 62


# Models
class InputDevice(db.Model):
    __tablename__ = "InputDevice"
    id = db.Column(db.Integer, primary_key=True)
    Manufacturer = db.Column(db.String(64))
    Model = db.Column(db.String(64))
    Type = db.Column(db.String(64))
    inputmapping = db.relationship('InputMapping', backref = 'InputDevice')

class OutputDevice(db.Model):
    __tablename__ = "OutputDevice"
    id = db.Column(db.Integer, primary_key=True)
    Manufacturer = db.Column(db.String(64))
    Model = db.Column(db.String(64))
    Type = db.Column(db.String(64))
    outputmapping = db.relationship('OutputMapping', backref = 'OutputDevice')

class StageBox(db.Model):
    __tablename__ = "StageBox"
    id = db.Column(db.Integer, primary_key=True)
    Inputs = db.Column(db.Integer)
    Outputs = db.Column(db.Integer)
    showstageboxes = db.relationship('ShowStageBox', backref = 'StageBox')

class Show(db.Model):
    __tablename__ = "Show"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(64))
    Venue = db.Column(db.String(64))
    Company = db.Column(db.String(64))
    Date_from = db.Column(db.Date())
    Date_to = db.Column(db.Date())
    showstageboxes = db.relationship('ShowStageBox', backref = 'Show')


class ShowStageBox(db.Model):
    __tablename__ = "ShowStageBox"
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer,db.ForeignKey('Show.id'))
    stagebox_id = db.Column(db.Integer,db.ForeignKey('StageBox.id'))

class InputMapping(db.Model):
    __tablename__ = "InputMapping"
    id = db.Column(db.Integer, primary_key=True)
    ShowStageBoxID = db.Column(db.Integer,db.ForeignKey('InputDevice.id'))
    Port = db.Column(db.Integer)
    InputID = db.Column(db.Integer)
    StripPosition = db.Column(db.Integer)
    Label = db.Column(db.String(64))

class OutputMapping(db.Model):
    __tablename__ = "OutputMapping"
    id = db.Column(db.Integer, primary_key=True)
    ShowStageBoxID = db.Column(db.Integer,db.ForeignKey('OutputDevice.id'))
    Port = db.Column(db.Integer)
    InputID = db.Column(db.Integer)
    StripPosition = db.Column(db.Integer)
    Label = db.Column(db.String(64))