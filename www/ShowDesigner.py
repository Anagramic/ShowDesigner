from flask import Flask, render_template,g,redirect,url_for
from jinja2 import Template
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#finds the directory this file file is stored under
basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] =\
    "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SSQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app)
def getdb():
    if "db" not in g:
        g.db = sqlite3.connect(os.path.join(basedir, "database.db"), detect_types=sqlite3.PARSE_DECLTYPES)

        g.db.row_factory = sqlite3.Row

    return g.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kit')
def kit():
    db = getdb()
    InputInv = db.execute(
        "SELECT Inputdevice.ID, InputType.Manufacturer, InputType.Model, InputType.Type FROM InputType, InputDevice WHERE InputDevice.InputID = InputType.InputID"
        ).fetchall()
    OutputInv = db.execute(
        "SELECT Outputdevice.ID, OutputType.Manufacturer, OutputType.Model, OutputType.Type FROM OutputType, OutputDevice WHERE OutputDevice.OutputID = OutputType.OutputID"
    ).fetchall()
    StageBoxInv = db.execute(
        "SELECT ID, Inputs, Outputs FROM StageBox"
    )
#    StageBoxes = StageBox.query.all()
#    InputDevices = InputDevice.query.all()
#    OutputDevices = OutputDevice.query.all()
#    return render_template('kit.html',InputDevices =  InputDevices,OutputDevices = OutputDevices,StageBoxes = StageBoxes)
    return render_template("kit.html",InDevices = InputInv, OutDevices = OutputInv, Stageboxes = StageBoxInv)
@app.route('/shows')
def shows():
    db = getdb()
    shows = db.execute(
        "SELECT ID,ShowName FROM Show"
    ).fetchall()
    return render_template('shows.html', shows=shows)

@app.route('/show/<showid>')
def show(showid):
    db = getdb()
    ShowName = db.execute(
        "SELECT Show.ShowName FROM Show WHERE ID = ?",[showid]
    ).fetchall()[0]["ShowName"]

    Inputs = db.execute(
        "SELECT InputDevice.ID, InputType.Manufacturer, InputType.Model, InputType.Type, InputDevice.BarcodeID FROM InputDevice, InputType, Show, ShowStageBox, InputMapping WHERE InputMapping.ShowStageBoxID = ShowStageBox.ID AND ShowStageBox.ShowID = Show.ID  AND InputMapping.InputID = InputDevice.ID AND InputDevice.InputID = InputType.InputID AND Show.ID = ?",[showid]
    ).fetchall()
    Outputs = db.execute(
        "SELECT OutputDevice.ID, OutputType.Manufacturer, OutputType.Model, OutputType.Type, OutputDevice.BarcodeID FROM OutputDevice, OutputType, Show, ShowStageBox, OutputMapping WHERE OutputMapping.ShowStageBoxID = ShowStageBox.ID AND ShowStageBox.ShowID = Show.ID  AND OutputMapping.OutputID = OutputDevice.ID AND OutputDevice.OutputID = OutputType.OutputID AND Show.ID = ?",[showid]
    ).fetchall()
    
    InPatch = db.execute(
        "SELECT InputMapping.Port, InputMapping.StripPosition, Inputmapping.Label, InputType.Manufacturer, InputType.Model, InputType.Type, ShowstageBox.ID, ShowStageBox.StageBoxID, InputMapping.ID FROM InputDevice, InputType, Show, ShowStageBox, InputMapping WHERE InputMapping.ShowStageBoxID = ShowStageBox.ID AND ShowStageBox.ShowID = Show.ID  AND InputMapping.InputID = InputDevice.ID AND InputDevice.InputID = InputType.InputID AND Show.ID = ?",[showid]
    ).fetchall()
    OutPatch = db.execute(
        "SELECT OutputMapping.Port, OutputMapping.StripPosition, Outputmapping.Label, OutputType.Manufacturer, OutputType.Model, OutputType.Type, OutputDevice.BarcodeID, ShowstageBox.ID, ShowStageBox.StageBoxID, OutputMapping.ID FROM OutputDevice, OutputType, Show, ShowStageBox, OutputMapping WHERE OutputMapping.ShowStageBoxID = ShowStageBox.ID AND ShowStageBox.ShowID = Show.ID  AND OutputMapping.OutputID = OutputDevice.ID AND OutputDevice.OutputID = OutputType.OutputID AND Show.ID = ?",[showid]
    ).fetchall()
    StageBox = db.execute(
        "SELECT StageBox.ID, StageBox.Inputs, StageBox.Outputs FROM StageBox, ShowStageBox WHERE ShowStageBox.StageBoxID = StageBox.ID AND ShowStageBox.ShowID = ?",[showid]
    ).fetchall()
    StageBoxes = []
    for Box in StageBox:
        BoxData = {"ID":Box["ID"],"Inputs":[],"Outputs":[]}

        for i in range(Box["Inputs"]):
            PortData = {"Port":i+1, "Manufacturer":"","Model":"","Type":"","Label":""}
            BoxData["Inputs"].append(PortData)
               
        for i in range(Box["Outputs"]):
            PortData = {"Port":i+1, "Manufacturer":"","Model":"","Type":"","Label":""}
            BoxData["Outputs"].append(PortData)


        for device in InPatch:
            if device["StageBoxID"] == Box["ID"]:
                PortData = BoxData["Inputs"][device["Port"]-1]
                PortData["Manufacturer"] = device["Manufacturer"]
                PortData["Model"] = device["Model"]
                PortData["Type"] = device["Type"]
                PortData["Label"] = device["Label"]
                PortData["InputMappingID"] = device[8]
        
        for device in OutPatch:
            if device["StageBoxID"] == Box["ID"]:
                PortData = BoxData["Outputs"][device["Port"]-1]
                PortData["Manufacturer"] = device["Manufacturer"]
                PortData["Model"] = device["Model"]
                PortData["Type"] = device["Type"]
                PortData["Label"] = device["Label"]
                PortData["OutputMappingID"] = device[8]

        StageBoxes.append(BoxData)
    return render_template('show.html', InDevicesKit = Inputs, OutDevicesKit = Outputs, InDevicesPatch = InPatch, OutDevicesPatch = OutPatch, ShowName = ShowName, StageBoxes = StageBoxes, showid=showid)

@app.route("/Remove_Input_Mapping/<InputMappingID>")
def Remove_Input_Mapping(InputMappingID):
    db = getdb()

    ShowID = db.execute("SELECT ShowStageBox.ShowID FROM InputMapping, ShowStageBox WHERE InputMapping.ID=? AND InputMapping.ShowStageBoxID=ShowStageBox.ID",[InputMappingID]).fetchall()[0]['ShowID']

    cur = db.cursor()

    cur.execute(
        "DELETE FROM InputMapping WHERE ID = ?",[InputMappingID]
    )

    db.commit()

    return redirect(url_for('show', showid=ShowID))    

@app.route("/Remove_Output_Mapping/<OutputMappingID>")
def Remove_Output_Mapping(OutputMappingID):
    db = getdb()

    ShowID = db.execute("SELECT ShowStageBox.ShowID FROM OutputMapping, ShowStageBox WHERE OutputMapping.ID=? AND OutputMapping.ShowStageBoxID=ShowStageBox.ID",[OutputMappingID]).fetchall()[0]['ShowID']

    cur = db.cursor()

    cur.execute(
        "DELETE FROM OutputMapping WHERE ID = ?",[OutputMappingID]
    )

    db.commit()

    return redirect(url_for('show', showid=ShowID))

@app.route('/RemoveShow/<ShowID>')
def RemoveShow(ShowID):
    db = getdb()
    sbID = db.execute(
        "SELECT ID FROM ShowStageBox WHERE ShowID = ?",[ShowID]
    ).fetchall()

    cur = db.cursor()
    for i in sbID:
        cur.execute(
            "DELETE FROM OutputMapping WHERE ShowStageBoxID = ?",[i['ID']]
        )
        cur.execute(
            "DELETE FROM InputMapping WHERE ShowStageBoxID = ?",[i['ID']]
        )

    cur.execute(
        "DELETE FROM ShowStageBox WHERE ShowID = ?",[ShowID]
    )
    cur.execute(
        "DELETE FROM show WHERE ID = ?",[ShowID]
    )
    db.commit()
    return redirect("/shows")

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
# class InputDevice(db.Model):
#     __tablename__ = "InputDevice"
#     id = db.Column(db.Integer, primary_key=True)
#     Manufacturer = db.Column(db.String(64))
#     Model = db.Column(db.String(64))
#     Type = db.Column(db.String(64))
#     inputmapping = db.relationship('InputMapping', backref = 'InputDevice')

# class OutputDevice(db.Model):
#     __tablename__ = "OutputDevice"
#     id = db.Column(db.Integer, primary_key=True)
#     Manufacturer = db.Column(db.String(64))
#     Model = db.Column(db.String(64))
#     Type = db.Column(db.String(64))
#     outputmapping = db.relationship('OutputMapping', backref = 'OutputDevice')

# class StageBox(db.Model):
#     __tablename__ = "StageBox"
#     id = db.Column(db.Integer, primary_key=True)
#     Inputs = db.Column(db.Integer)
#     Outputs = db.Column(db.Integer)
#     showstageboxes = db.relationship('ShowStageBox', backref = 'StageBox')

# class Show(db.Model):
#     __tablename__ = "Show"
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(64))
#     Venue = db.Column(db.String(64))
#     Company = db.Column(db.String(64))
#     Date_from = db.Column(db.Date())
#     Date_to = db.Column(db.Date())
#     showstageboxes = db.relationship('ShowStageBox', backref = 'Show')


# class ShowStageBox(db.Model):
#     __tablename__ = "ShowStageBox"
#     id = db.Column(db.Integer, primary_key=True)
#     show_id = db.Column(db.Integer,db.ForeignKey('Show.id'))
#     stagebox_id = db.Column(db.Integer,db.ForeignKey('StageBox.id'))
 
# class InputMapping(db.Model):
#     __tablename__ = "InputMapping"
#     id = db.Column(db.Integer, primary_key=True)
#     ShowStageBoxID = db.Column(db.Integer,db.ForeignKey('InputDevice.id'))
#     Port = db.Column(db.Integer)
#     InputID = db.Column(db.Integer)
#     StripPosition = db.Column(db.Integer)
#     Label = db.Column(db.String(64))

# class OutputMapping(db.Model):
#     __tablename__ = "OutputMapping"
#     id = db.Column(db.Integer, primary_key=True)
#     ShowStageBoxID = db.Column(db.Integer,db.ForeignKey('OutputDevice.id'))
#     Port = db.Column(db.Integer)
#     InputID = db.Column(db.Integer)
#     StripPosition = db.Column(db.Integer)
#     Label = db.Column(db.String(64))