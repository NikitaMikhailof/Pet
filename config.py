from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import session, abort
from models import User, Order, UserBasket, Products 
from models import UserView, OrderView, UserBasketView, ProductsView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class UserView(ModelView):  
    def is_accessible(self):
       if "logged_in" in session:
           return True 
       else:
           abort(403)
           
    can_delete = True
    column_list = [ "username", "email", "name", 
                    "telephone", "name", "age",
                    "name", "created_at", "updated_on",
                    "is_active" ,"address", "password"]  

class ProductsView(ModelView):
    def is_accessible(self):
       if "logged_in" in session:
           return True 
       else:
           abort(403)

    can_delete = True
    column_list = [ "product_name", "description", "price"]    

class OrderView(ModelView):  
    def is_accessible(self):
       if "logged_in" in session:
           return True 
       else:
           abort(403)

    can_delete = True
    column_list = [ "quantity", "user", "product", 
                   "total_price", "time_buy", "type_payment",
                   "message"]
    
class UserBasketView(ModelView):
    def is_accessible(self):
       if "logged_in" in session:
           return True 
       else:
           abort(403)

    can_delete = True
    column_list = [ "user_basket", "product_basket", 
                   "quantity", "price"]
        