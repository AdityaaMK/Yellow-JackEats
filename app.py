from flask import *
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from get_menu import *

app = Flask(__name__)
app.secret_key = "top secret"
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
allOrderDisplay = []

@app.before_request
def make_session_permanent():
    session.permanent = True

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
    phone = db.Column(db.String(100), nullable=False)
    food = db.Column(db.String(300))
    from_loc = db.Column(db.String(100))
    to_loc = db.Column(db.String(100))
    deliverer_name = db.Column(db.String(100))
    deliverer_phone = db.Column(db.String(100))
    
    def get_id(self):
        return(self._id)

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password

class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw = {"placeholder":"Name"})
    email = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw = {"placeholder":"Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw = {"placeholder":"Password"})
    phone = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw = {"placeholder":"Phone Number"})
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
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():
        #hash password to encrypt it
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, phone=form.phone.data, food="", from_loc="", to_loc="", deliverer_name="", deliverer_phone="")
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
                session['name'] = user.name
                session['phone']=user.phone
                session['logged_in']=True
                session['email']=form.email.data
                return redirect(url_for('home'))
                
    return render_template("login.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session['logged_in']=False
    session['email']=""
    return redirect(url_for('login'))

@app.route("/home")
@login_required
def home():
    if session.get('logged_in'):
        return render_template("home.html")
    return redirect(url_for("login"))

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    if session.get('logged_in'):
        user = User.query.filter_by(email=session['email'])
        if request.method == "POST":
            data = dict(request.form)
            from_loc = data.pop("from_loc")
            if (not list(data.keys())): 
                print("Location: ", from_loc)
                try:
                    foods = get_menu(request.form.get("from_loc"), "lunch")
                    if foods:
                        return render_template("order.html", from_loc=from_loc, foods=foods)
                except:
                    return render_template("order.html", from_loc=from_loc)
            else:
                to_loc = data.pop('to_loc')
                food_list = list(data.keys())
                # print("Location: ", loc)
                # session['food_list'] = food_list
                # session['loc'] = loc
                # user.food = ','.join(map(str, food_list))
                # user.from_loc = loc
                # user.to_loc = to_loc
                # new_user = User(name=session['name'], email=user.email.data, password=user.password.data, phone=user.phone.data, food=user.food.data, from_loc="", to_loc="", deliverer_name="", deliverer_phone="")
                # User.query.filter_by(email=session['email']).delete()  
                # db.session.commit()              
                # db.session.add(new_user)
                query = db.session.query(User)
                # print(query)
                orderDisplay = {}
                locationConversions = {"blue-donkey":"Blue Donkey",
                    "brittain":"Brittain",
                    "chick-fil-a":"Chick Fil",
                    "wing-zone":"Wing Zone",
                    "kaldis-coffee":"Kaldis Coffee", 
                    "panda-express":"Panda Express", 
                    "north-ave-dining":"North Ave",
                    "ramblin-coffee-sweets":"Ramblin Coffee Sweets",
                    "rising-roll":"Rising Roll",
                    "the-dive":"The Dive",
                    "twisted-taco": "Twisted Taco",
                    "west-village":"Willage"}
                for x in query:
                    if x.email == session['email']:
                        orderDisplay = {'name':x.name, 'email':x.email, 'phone_number':x.phone, 'food':food_list, 'to_loc':to_loc, 'from_loc':locationConversions.get(from_loc), 'payment':"$2", 'deliverer_name':"TBA", 'deliverer_phone':"TBA"}
                        allOrderDisplay.append({'name':x.name, 'email':x.email, 'phone_number':x.phone, 'food':food_list, 'to_loc':to_loc, 'from_loc':locationConversions.get(from_loc), 'payment':"$2", 'deliverer_name':"TBA", 'deliverer_phone':"TBA"})
                # for entry in orderDisplay:
                #     if entry['email'] == session['email']:
                #         entry['food'] = food_list
                #         entry['loc'] = to_loc
                session['orderDisplay'] = orderDisplay
                print(session['orderDisplay'])
                print(allOrderDisplay)
                return redirect(url_for('checkout'))
        return render_template("order.html")
    return redirect(url_for('login'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if session.get('logged_in'):
        if request.method == "POST":
            return redirect(url_for('order_details'))
        print("ORDERS: ", session['orderDisplay'])
        return render_template("checkout.html", orders=session['orderDisplay'])
    return redirect(url_for('login'))

@app.route('/order_details', methods=['GET', 'POST'])
@login_required
def order_details():
    if session.get('logged_in'):
        email = session["email"]
        order = {}
        for x in allOrderDisplay:
            if email == x.get("email"):
                order = x
        # return render_template("order_details.html", orders=session['orderDisplay'])
        return render_template("order_details.html", orders=order)
    return redirect(url_for('login'))

@app.route('/deliver', methods=['GET', 'POST'])
@login_required
def deliver():
    if session.get('logged_in'):
        if request.method == "POST":
            return redirect(url_for('confirmation'))
        return render_template("deliver.html", orders=allOrderDisplay)
    return redirect(url_for('login'))

@app.route('/confirmation', methods=['GET', 'POST'])
@login_required
def confirmation():
    if session.get('logged_in'):
        if request.method == "POST":
            email = request.form.get('email')
            delivery_order = {}
            for x in allOrderDisplay:
                if email == x.get("email"):
                    delivery_order = x
        return render_template("confirmation.html", order=delivery_order)
    return redirect(url_for('login'))

@app.route('/deliver_details', methods=['GET', 'POST'])
@login_required
def deliver_details():
    if session.get('logged_in'):
        if request.method == "POST":
            email = request.form.get('email')
            delivery_order = {}
            for x in allOrderDisplay:
                if email == x.get("email"):
                    x["deliverer_name"] = session["name"]
                    x["deliverer_phone"] = session["phone"]
                    delivery_order = x
        return render_template("deliver_details.html", order=delivery_order)
    return redirect(url_for('login'))

@app.route("/analytics")
def analytics():
    labels = [
        'Spaghetti', 'Mushroom Pizza', 'Chocolate Chip Cookie', 'Roasted Cauliflowers'
    ]

    values = [
        34, 23, 25, 15
    ]
    bar_labels=labels
    bar_values=values
    return render_template('analytics.html', title='Yellow JackEats Analytics', max=50, labels=bar_labels, values=bar_values)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)