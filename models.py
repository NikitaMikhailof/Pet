from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin


db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    is_active = db.Column(db.Boolean, default=True)   

    def __repr__(self):
        return f'User({self.username}, {self.email})'

    def check_password(self,  password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
	    self.password = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id) 
    

    

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    descriptions = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Product({self.product_name}, {self.price})'    

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.String(100), db.ForeignKey('products.id')) # сделать связь многие ко многим
    time_buy = db.Column(db.DateTime, default=None)
    quantity = db.Column(db.Integer, default=1)
    

    def __repr__(self):
        return f'User_basket({self.user_id}, {self.product_id}, {self.time_buy}, {self.quantity}'

    

    
   

