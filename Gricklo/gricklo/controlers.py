from flask_wtf import form
from gricklo import app , db
import os
from flask import render_template,redirect,url_for,request,flash
from werkzeug.utils import secure_filename
from gricklo.models import *
from gricklo.forms import RegistrationForm,LoginForm
from gricklo.imageupload import save_picture
from passlib.hash import sha256_crypt

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

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        customer = Customer.filter_by(username=username.data)
        if customer:
            real_password = customer['password']
            if sha256_crypt.verify(password,real_password):
                flash("Login is succsess..","success")
                return redirect(url_for("index"))
            else:
                flash("Password is wrong","danger")
                return redirect(url_for("login"))




    
    return render_template("login.html",form=form)

@app.route("/register", methods=["GET","POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        customer = Customer(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            password = sha256_crypt.encrypt(form.password.data),
            phone = form.phone.data,
            image = save_picture(form.image.data)

        )
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html" , form=form)


#Admin
@app.route("/admin")
def dashboard():
    return render_template("admin/admin.html")


@app.route('/admin/customerlist')
def customerlist():
    customers = Customer.query.all()
    return render_template('admin/customerlist.html', customers=customers)
    


#Restaurant add
@app.route("/admin/resadd", methods=["GET","POST"])
def restaurant_add():
    cities =City.query.all()
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        restaurant = Restaurant(
            title = request.form['title'],
            location = request.form['location'],
            image = filename,
            city = request.form['city']

        )
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for("restaurant_list"))
    return render_template("admin/resadd.html", cities=cities)

@app.route('/admin/reslist')
def restaurant_list():
    restaurants = Restaurant.query.all()
    
    return render_template('admin/reslist.html', restaurants=restaurants)


@app.route('/admin/resedit/<int:id>' ,methods=["GET","POST"])
def restaurant_edit(id):
    cities =City.query.all()
    restaurants = Restaurant.query.get_or_404(id)
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        restaurants.title= request.form['title']
        restaurants.location = request.form['location']
        restaurants.image = filename
        restaurants.city = request.form['city']
        db.session.commit()
        return redirect(url_for("restaurant_list"))

    return render_template('admin/resedit.html', restaurants=restaurants , cities = cities)

@app.route('/admin/resdelete/<int:id>')
def restaurant_delete(id):
    restaurants = Restaurant.query.get_or_404(id)
    db.session.delete(restaurants)
    db.session.commit()
    return redirect(url_for("restaurant_list"))

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
        return redirect(url_for("city_list"))
    return render_template("admin/cityadd.html")

@app.route('/admin/citylist')
def city_list():
    cities = City.query.all()
    return render_template('admin/citylist.html', cities=cities)


@app.route('/admin/cityedit/<int:id>' ,methods=["GET","POST"])
def city_edit(id):
    
    cities = City.query.get_or_404(id)
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cities.title= request.form['title']
        cities.image = filename
        db.session.commit()
        return redirect(url_for("city_list"))

    return render_template('admin/cityedit.html',  cities = cities)

@app.route('/admin/citydelete/<int:id>')
def city_delete(id):
    cities = City.query.get_or_404(id)
    db.session.delete(cities)
    db.session.commit()
    return redirect(url_for("city_list"))

#blog
@app.route("/admin/blogadd", methods=["GET","POST"])
def blog_add():
    categoris = BlogCategory.query.all()
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog = Blog(
            title = request.form['title'],
            short_description = request.form['short_description'],
            image = filename,
            city = request.form['city']

        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("blog_list"))
    return render_template("admin/blogadd.html", categoris=categoris )

@app.route('/admin/bloglist')
def blog_list():
    blogs = Blog.query.all()
    
    return render_template('admin/reslist.html', blogs=blogs )


@app.route('/admin/blogedit/<int:id>' ,methods=["GET","POST"])
def blog_edit(id):
    categories =Blog.query.all()
    blogs = Restaurant.query.get_or_404(id)
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blogs.title= request.form['title']
        blogs.location = request.form['location']
        blogs.image = filename
        blogs.city = request.form['city']
        db.session.commit()
        return redirect(url_for("restaurant_list"))

    return render_template('admin/blogedit.html', blogs=blogs , categories = categories)

@app.route('/admin/blogdelete/<int:id>')
def blog_delete(id):
    blogs = Blog.query.get_or_404(id)
    db.session.delete(blogs)
    db.session.commit()
    return redirect(url_for("blog_list"))


#blogcategory
@app.route("/admin/categoryadd", methods=["GET","POST"])
def category_add():
    if request.method == "POST":
        category = BlogCategory(
            title = request.form['title']
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("category_list"))
    return render_template("admin/categoryadd.html")

@app.route('/admin/categorylist')
def category_list():
    categories = BlogCategory.query.all()
    return render_template('admin/categorylist.html', categories=categories)

@app.route('/admin/categoryedit/<int:id>' ,methods=["GET","POST"])
def category_edit(id):
    categories =BlogCategory.query.all()
    if request.method == "POST":
        categories.title= request.form['title']
        db.session.commit()
        return redirect(url_for("category_list"))

    return render_template('admin/categoryedit.html', categories = categories)

@app.route('/admin/categorydelete/<int:id>')
def category_delete(id):
    categories = BlogCategory.query.get_or_404(id)
    db.session.delete(categories)
    db.session.commit()
    return redirect(url_for("category_list"))
