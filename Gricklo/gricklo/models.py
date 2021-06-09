from gricklo import db , login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(25), unique=True, nullable=False)
    image = db.Column(db.String(20),default='image.png')
    orders = db.relationship('Order',backref='order',lazy=True, cascade="all,delete")
    comments =db.relationship('Comment',backref='comment',lazy=True, cascade="all,delete")
    blogs = db.relationship('Blog',backref='blog',lazy=True, cascade="all,delete")
    posts = db.relationship('UserPost',backref='blog',lazy=True, cascade="all,delete")
    
    def __repr__(self) -> str:
        return f"User:{self.username}"

class UserPost(db.Model, UserMixin):
    __tablename__ = "userpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    short_description = db.Column(db.String(50),nullable=False)
    blog_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(50),nullable=False)
    image = db.Column(db.String(20), default = "default.png")
    author =db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"UserPost:{self.title}"



class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    description = db.Column(db.Text,nullable=False)
    comment_posted=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"Comment:{self.title}"

class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    short_description = db.Column(db.String(50),nullable=False)
    description = db.Column(db.Text, nullable=False)
    blog_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(20), default = "default.png")
    category = db.Column(db.Integer, db.ForeignKey('blogcategory.id'), nullable=False)
    customer =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self) -> str:
        return f"Blog :{self.title}"

class BlogCategory(db.Model):
    __tablename__ = "blogcategory"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50),nullable = False)
    blog =db.relationship('Blog', backref='blogs',lazy=True)
    def __repr__(self) -> str:
        return f"Blog Category:{self.title}"

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50),nullable = False)
    order = db.relationship("Order", backref='orders',lazy=True )
    def __repr__(self) -> str:
        return f"Category:{self.title}"


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    short_description = db.Column(db.String(127),nullable=False)
    description = db.Column(db.Text,nullable=False)
    price = db.Column(db.Float,nullable=False)
    image = db.Column(db.String(20),default='image.png')
    customer_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    category = db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
    def __repr__(self) -> str:
        return f"Order:{self.title}"

class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    location = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(20),default='image.png')
    city = db.Column(db.Integer,db.ForeignKey('city.title'),nullable=False)
    def __repr__(self) -> str:
        return f"Restaurant:{self.title}"

class City(db.Model):
    __tablename__ = "city"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False,unique=True)
    image = db.Column(db.String(20),default='image.png')
    restaurant =db.relationship(Restaurant, backref='restaurant',lazy=True ,cascade="all,delete")
    def __repr__(self) -> str:
        return f"City:{self.title}"
