from flask import *
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "top secret"
app.permanent_session_lifetime = timedelta(minutes=5)
# users is the name of table we are referencing 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# run "from app import db" and then "db.create_all()"
# watch vid at 13-14 min mark to test database
# https://www.youtube.com/watch?v=71EU8gnZqZQ
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # primary key is set to True bc we are going to use id to reference our objects
    # every object will have unique id to reference
    # id will be automatically created since it is primary key
    _id = db.Column("id", db.Integer, primary_key=True)
    # nullable false means field is required
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    def get_id(self):
        return(self._id)

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password

class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw = {"placeholder":"Name"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw = {"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw = {"placeholder":"Password"})
    submit = SubmitField("Register")
    def validate_username(self, email):
        existing_user_email = User.query.filter_by(email = email.data).first()
        if existing_user_email:
            raise ValidationError("That email exists already. Please choose a different one.")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw = {"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw = {"placeholder":"Password"})
    submit = SubmitField("Login")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        #hash password to encrypt it
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('order'))
 
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/order', methods=['GET', 'POST'])
def order():
    return render_template("order.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)