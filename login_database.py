from flask import *
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitF


app = Flask(__name__)
app.secret_key = "top secret"
app.permanent_session_lifetime = timedelta(minutes=5)
# users is the name of table we are referencing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# run "from app import db" and then "db.create_all()"
# watch vid at 13-14 min mark to test database
# https://www.youtube.com/watch?v=71EU8gnZqZQ
db = SQLAlchemy(app)

class users(db.Model, UserMixin):
    # primary key is set to True bc we are going to use id to reference our objects
    # every object will have unique id to reference
    _id = db.Column("id", db.Integer, primary_key=True)
    # nullable false means field is required
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    # id will be automatically created since it is primary key

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password

class RegisterForm(Flask):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)])


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    pass
    

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)