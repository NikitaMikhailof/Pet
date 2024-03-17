from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)   

    
    

    def __repr__(self):
        return f'User_profile({self.username}, {self.password}, {self.email}, {self.name}, {self.age}, {self.address}, {self.created_at})'


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



class LoginUser():
    def get_email(email):
        user = User.query.filter_by(email=email).first()
        return f'{user.email}'

    def is_user(login):
        user = User.query.filter_by(username=login).first()
        if user:
            return True
        return False  
    
    def get_psw(pasw):
        user = User.query.filter_by(password=pasw).first()
        return f'{user['password']}'


