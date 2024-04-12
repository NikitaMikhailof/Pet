from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin
from flask import url_for
import sqlite3
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)

    orders = db.relationship("Order", back_populates="user")

    # avatar = db.Column(db.LargeBinary)
    avatar = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    is_active = db.Column(db.Boolean, default=True) 
 

    def __repr__(self):
        return f'User({self.username}, {self.email}, {self.id}, {self.telephone}, {self.address})'

    def check_password(self,  password):
        return check_password_hash(self.password, password)

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id) 
    
    def is_authenticated(self):
        return True
    
    def verifyExt(self, filename):
        ALLOWED_EXTESIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        ext = filename.rsplit('.', 1)[1].lower()
        if ext in ALLOWED_EXTESIONS:
            return True
        return False
    
    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.avatar = binary
            db.session.commit()
        except sqlite3.Error as e:
            print('Ошибка обновления аватара в БД: ' + str(e))  
            return False
        return True  
    
    def getAvatar(self):
        img = None
        if not self.avatar:
            try:
                with open(url_for('static', filename='img/avatar/avatarka.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print('Не найден аватарка по умолчанию: ' + str(e))
        else:
            img = self.avatar 
        return img  

    def set_password(self, password):
	    self.password = generate_password_hash(password)

      
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    descriptions = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Integer, nullable=False)

    orders = db.relationship("Order", back_populates="products")

    def __repr__(self):
        return f'Product({self.product_name}, {self.price})'    
    

class UserBasket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_title = db.Column(db.String(30))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer)
    
    def __repr__(self):
        return f'User_basket({self.user_id}, {self.product_title}, {self.price}, {self.quantity}'    
    


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="orders")
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    products = db.relationship("Products", back_populates="orders")
    time_buy = db.Column(db.DateTime, default=datetime.now().replace (microsecond=0))
    quantity = db.Column(db.Integer) 
    total_price = db.Column(db.Integer) 
    message = db.Column(db.String(200))
    type_payment = db.Column(db.String(20))


class OrderView(ModelView):  
    can_delete = True
    form_columns = ['user', 'products', 'quantity','message',
                      'type_payment', 'total_price',
                      'type_payment', 'time_buy']

    def __repr__(self):
        return f'User_basket({self.user}, {self.product}, {self.time_buy}, {self.total_price}'

    

    
   

