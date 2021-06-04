from datetime import datetime
from os import name
from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from os.path import join, dirname, realpath, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')


app = Flask(__name__)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
# from imageupload import save_picture


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(25), unique=True, nullable=False)
    image = db.Column(db.String(20),default='image.png')
    orders = db.relationship('Order',backref='owner',lazy=True)
    commets =db.relationship('Comment',backref='owner',lazy=True)
    
    def __repr__(self) -> str:
        return f"Customer:{self.username}"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)
    description = db.Column(db.Text,nullable=False)
    comment_posted=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"Customer:{self.title}"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    short_description = db.Column(db.String(127),nullable=False)
    description = db.Column(db.Text,nullable=False)
    price = db.Column(db.Float,nullable=False)
    image = db.Column(db.String(20),default='image.png')
    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)
    def __repr__(self) -> str:
        return f"Title:{self.title}"

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    location = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(20),default='image.png')
    
    def __repr__(self) -> str:
        return f"Customer:{self.title}"

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    image = db.Column(db.String(20),default='image.png')
    
    def __repr__(self) -> str:
        return f"Customer:{self.title}"




@app.route("/")
def index():
    restaurants = Restaurant.query.all()
    citys = City.query.all()
    return render_template("index.html",restaurants=restaurants, citys= citys)

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blogdetails")
def blogdetails():
    return render_template("blogdetails.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/listing")
def listing():
    return render_template("listing.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def signup():
    return render_template("register.html")


#Dashboard
@app.route("/admin")
def dashboard():
    return render_template("admin/admin.html")
@app.route("/admin/customeradd", methods=["GET","POST"])
def customer_add():
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        customer = Customer(
            name = request.form['name'],
            username = request.form['username'],
            email = request.form['email'],
            phone = request.form['phone'],
            image = filename,

        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for("customeredit"))
    return render_template("admin/customeradd.html")

@app.route('/admin/customeredit')
def customeredit():
    customers = Customer.query.all()
    return render_template('admin/customeredit.html', customers=customers)
    


#Restaurant add
@app.route("/admin/resadd", methods=["GET","POST"])
def restaurant_add():
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        restaurant = Restaurant(
            title = request.form['title'],
            location = request.form['location'],
            image = filename,

        )
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for("restaurant_edit"))
    return render_template("admin/resadd.html")

@app.route('/admin/resedit')
def restaurant_edit():
    restaurants = Restaurant.query.all()
    return render_template('admin/resedit.html', restaurants=restaurants)

#city add
@app.route("/admin/cityadd", methods=["GET","POST"])
def city_add():
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        city = City(
            title = request.form['title'],
            image = filename,

        )
        db.session.add(city)
        db.session.commit()
        return redirect(url_for("city_edit"))
    return render_template("admin/cityadd.html")

@app.route('/admin/cityedit')
def city_edit():
    citys = City.query.all()
    return render_template('admin/cityedit.html', citys=citys)
if __name__ == "__main__":
    app.run(debug=True)
