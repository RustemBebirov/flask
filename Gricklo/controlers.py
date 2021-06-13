from werkzeug import datastructures
from gricklo import app , db , bcrypt
import os
from flask import render_template,redirect,url_for,request,flash
from werkzeug.utils import secure_filename
from gricklo.models import *
from gricklo.forms import RegistrationForm, LoginForm ,UserPostForm
from gricklo.imageupload import save_picture
from flask_login import login_user, logout_user,login_required,current_user

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
    categories=BlogCategory.query.all()
    posts = UserPost.query.all()
    blogs=Blog.query.all()
    return render_template("blog.html" , blogs=blogs , categories=categories, posts= posts)

@app.route("/blogdetails/<int:id>", methods=["GET","POST"])
def blogdetails(id):
    categories=BlogCategory.query.all()
    posts = UserPost.query.all()
    blog=Blog.query.get_or_404(id)
    comments = Comment.query.filter_by(blogs=id)
    if request.method == "POST":
        comment = Comment(
            author = request.form['author'],
            email = request.form['email'],
            comment = request.form['comment'],
            blogs = blog.id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blogdetails', id=blog.id))
    return render_template("blogdetails.html" , blog= blog, categories=categories, posts=posts,comments = comments)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/listing")
def listing():
    restaurants = Restaurant().query.all()
    return render_template("listing.html" , restaurants= restaurants)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            
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
        user_password = form.password.data
        parol_hashed = bcrypt.generate_password_hash(user_password).decode("utf-8")
        user = User(
            name = form.name.data,
            email = form.email.data,
            password = parol_hashed,
            image = save_picture(form.image.data)

        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html" , form=form)

@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    user_posts = UserPost.query.filter_by(user=current_user.name)
    form = UserPostForm()
    if form.validate_on_submit():
        user_post=UserPost(
            title = form.title.data,
            short_description = form.short_description.data,
            content = form.content.data,
            image = save_picture(form.image.data),
            user = current_user.name,
        )
        db.session.add(user_post)
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("account.html" , form=form , user_posts=user_posts)

@app.route('/postedit/<int:id>' ,methods=["GET","POST"])
def post_edit(id):
    user_posts = UserPost.query.get_or_404(id)
    form = UserPostForm()
    if request.method == "POST":
        user_posts.title= form.title.data
        user_posts.short_description = form.short_description.data
        user_posts.content = form.content.data
        user_posts.image = save_picture(form.image.data)
        db.session.commit()
        return redirect(url_for("account"))

    return render_template('postedit.html' ,form=form)


@app.route('/postdelete/<int:id>')
def post_delete(id):
    user_post = UserPost.query.get_or_404(id)
    db.session.delete(user_post)
    db.session.commit()
    return redirect(url_for("account"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#Admin
@app.route("/admin")
@login_required
def dashboard():
    
    return render_template("admin/admin.html")


@app.route('/admin/customerlist')
def customerlist():
    users = User.query.all()
    return render_template('admin/customerlist.html', users=users)
    


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
            status = request.form['status'],
            phone=request.form['phone'],
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
        restaurants.status = request.form['status']
        restaurants.phone = request.form['phone']
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
    categories = BlogCategory.query.all()
    customers = User.query.all()
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blog = Blog(
            title = request.form['title'],
            short_description = request.form['short_description'],
            description = request.form['description'],
            image = filename,
            category = request.form['category'],

        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("blog_list"))
    return render_template("admin/blogadd.html", categories=categories, customers=customers )

@app.route('/admin/bloglist')
def blog_list():
    blogs = Blog.query.all()
    
    return render_template('admin/bloglist.html', blogs=blogs )


@app.route('/admin/blogedit/<int:id>' ,methods=["GET","POST"])
def blog_edit(id):
    categories = BlogCategory.query.all()
    customers = User.query.all()
    blogs = Blog.query.get_or_404(id)
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        blogs.title= request.form['title']
        blogs.short_description = request.form['short_description']
        blogs.description = request.form['description']
        blogs.image = filename
        blogs.category = request.form['category']
        db.session.commit()
        return redirect(url_for("blog_list"))

    return render_template('admin/blogedit.html', blogs=blogs , categories = categories,customers=customers)

@app.route('/admin/blogdelete/<int:id>')
def blog_delete(id):
    blogs = Blog.query.get_or_404(id)
    db.session.delete(blogs)
    db.session.commit()
    return redirect(url_for("blog_list"))


#category
@app.route("/admin/categoryadd", methods=["GET","POST"])
def category_add():
    if request.method == "POST":
        category = Category(
            title = request.form['title']
        )
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("category_list"))
    return render_template("admin/categoryadd.html")

@app.route('/admin/categorylist')
def category_list():
    categories = Category.query.all()
    return render_template('admin/categorylist.html', categories=categories)

@app.route('/admin/categoryedit/<int:id>' ,methods=["GET","POST"])
def category_edit(id):
    categories = Category.query.get_or_404(id)
    if request.method == "POST":
        categories.title= request.form['title']
        db.session.commit()
        return redirect(url_for("category_list"))

    return render_template('admin/categoryedit.html', categories = categories)

@app.route('/admin/categorydelete/<int:id>')
def category_delete(id):
    categories = Category.query.get_or_404(id)
    db.session.delete(categories)
    db.session.commit()
    return redirect(url_for("category_list"))

#blog category
@app.route("/admin/blogcategoryadd", methods=["GET","POST"])
def blogcategory_add():
    if request.method == "POST":
        blogcategory =BlogCategory(
            title = request.form['title']
        )
        db.session.add(blogcategory)
        db.session.commit()
        return redirect(url_for("blogcategory_list"))
    return render_template("admin/blogcategoryadd.html")


@app.route('/admin/blogcategorylist')
def blogcategory_list():
    blogcategories = BlogCategory.query.all()
    return render_template('admin/blogcategorylist.html', blogcategories=blogcategories)

@app.route('/admin/blogcategoryedit/<int:id>' ,methods=["GET","POST"])
def blogcategory_edit(id):
    blogcategories = BlogCategory.query.get_or_404(id)
    if request.method == "POST":
        blogcategories.title= request.form['title']
        db.session.commit()
        return redirect(url_for("blogcategory_list"))

    return render_template('admin/blogcategoryedit.html', blogcategories = blogcategories)

@app.route('/admin/blogcategorydelete/<int:id>')
def blogcategory_delete(id):
    blogcategories = BlogCategory.query.get_or_404(id)
    db.session.delete(blogcategories)
    db.session.commit()
    return redirect(url_for("blogcategory_list"))
