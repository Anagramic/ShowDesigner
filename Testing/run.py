from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)



@app.route("/")
def template_test():
    return render_template('template.html')



if __name__ == '__main__':
    app.run(debug=True)