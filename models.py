from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from sqlalchemy import create_engine, Connection, MetaData


app = Flask(__name__)
db = SQLAlchemy()
metadata = MetaData()


def connection_database():
    engine = create_engine(url='sqlite:///mydatabase.db') 
    return engine.connect()


class User_profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



    def __repr__(self):
        return f'User_profile({self.username}, {self.password}, {self.email}, {self.name}, {self.age}, {self.age}, {self.created_at})'


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Product({self.product_name}, {self.price})'    


class User_basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100), db.ForeignKey('products.id'), unique=True)
    time_buy = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))

    def __repr__(self):
        return f'User_basket({self.username}, {self.product_name}, {self.price}, {self.time_buy}'


class LoginUser():
    def get_email(email):
        user = User_profile.query.filter_by(email=email).first()
        return f'{user.email}'

    def is_user(login):
        user = User_profile.query.filter_by(username=login).first()
        if user:
            return True
        return False  
    
    def get_psw(pasw):
        user = User_profile.query.filter_by(password=pasw).first()
        return f'{user.password}'


