from flask import *
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)
app.secret_key = "top secret"
# orders is the name of table we are referencing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# run "from app import db" and then "db.create_all()"
# watch vid at 13-14 min mark to test database
# https://www.youtube.com/watch?v=71EU8gnZqZQ
db = SQLAlchemy(app)

class orders(db.Model):
    # primary key is set to True bc we are going to use id to reference our objects
    # every object will have unique id to reference
    # id will be automatically created since it is primary key
    _orderId = db.Column("id", db.Integer, primary_key=True)
    # nullable false means field is required
    food = db.Column(db.String(1000), nullable = False)
    fromLocation = db.Column(db.String(1000), nullable = False)
    toLocation = db.Column(db.String(1000), nullable = False)
    driverName = db.Column(db.String(100), nullable = False)
    driverNumber = db.Column(db.Integer(9), nullable = False)
    userName = db.Column(db.String(100), nullable = False)
    userNumber = db.Column(db.Integer(9), nullable = False)

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password

class OrderForm(FlaskForm):
    food = StringField(validators=[InputRequired(), Length(min=4, max=20)])

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/order")
# def order():
#     return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)