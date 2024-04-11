from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, make_response
from models import db, User, Products, Order, UserBasket
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PasswordRecoveryForm, СhangePassword
from forms import AccountRecoveryForm, UserProfile, Basket, BasketPositionDelete, MessageOrder
from passw_recovery import send_email
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
UPLOAD_FOLDER = 'static/img/avatar/'
MAX_CONTENT_LENGTH = 1024 * 1024 * 2



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    form_basket = Basket()
    products = Products().query.all()
    if form_basket.validate_on_submit() and current_user.is_authenticated:
        title = form_basket.title.data
        count = form_basket.count.data
        product = Products.query.filter_by(product_name=title).first() 
        total_price = int(product.price) * int(count)
        user = User().query.filter_by(username=current_user.username).first()
        new_basket = UserBasket(user_id=user.id, 
                                product_title=product.product_name, 
                                quantity=count, 
                                price=total_price)    
        db.session.add(new_basket)
        db.session.commit()     
    return render_template('index.html', products=products, form=form_basket)
 

 
@app.route('/registration/', methods=['POST', 'GET'])
def registration():  
    form_registration = RegistrationForm() 
    if request.method == 'POST': 
        if form_registration.validate_on_submit():
            email = form_registration.email.data
            user_name = form_registration.username.data
            hash = generate_password_hash(form_registration.password.data)
            user = User().query.filter_by(username=user_name).first()
            try:
                if user: 
                    flash('Пользователь с таким логином уже существует, придумайте новый', category='error')  
                else:
                    new_user = User(email=email, username=user_name, password=hash)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Регистрация прошла успешно', category='success')
                    return redirect(url_for('login'))
            except:
                     db.session.rollback()
        else:            
            flash('Данные введены не корректно', category='error')
    return  render_template('registration.html', form=form_registration)    


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
	    return redirect(url_for('user_profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active == True:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('user_profile', username=current_user.username))
        flash("Неверный логин / пароль", category='error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)
            

@app.route('/user_profile/<username>/', methods=['GET', 'POST'])
@login_required
def user_profile(username): 
    form = UserProfile()
    return render_template('user_profile.html', form=form, user=current_user)


@app.route('/user_profile//<username>/basket/', methods=['GET', 'POST'])
@login_required
def user_basket(username): 
    total = 0
    count_position = 0
    contents_basket = UserBasket().query.filter_by(user_id=current_user.id)
    
    for elem in contents_basket:
        total += elem.price
        count_position += elem.quantity

    form_delete_position = BasketPositionDelete() 
    address = current_user.address
    telephone = current_user.telephone

    if form_delete_position.validate_on_submit():
        title = form_delete_position.title.data
        for position in contents_basket:
            if position.product_title == title:
                remove_record = position
                db.session.delete(remove_record)
                db.session.commit() 
    return render_template('user_basket.html',
                            contents_basket=contents_basket,
                            total=total,
                            count_position=count_position,
                            username=current_user.username, 
                            form=form_delete_position)

@app.route('/user_profile/<username>/form_order/', methods=['GET', 'POST'])
@login_required
def form_order(username): 
    total = 0
    count_position = 0
    user_basket = UserBasket().query.filter_by(user_id=current_user.id)
    for elem in user_basket:
        total += elem.price
        count_position += elem.quantity  
           
    form_message = MessageOrder() 
    if form_message.validate_on_submit():
        type_payment = form_message.type_payment.data
        message = form_message.message.data
        for position in user_basket:
            order = Order(user_id = current_user.id,
                          product_id = position.product_title,
                          quantity = position.quantity,
                          message = message,
                          total_price = position.price,
                          type_payment = type_payment )
    
            db.session.add(order)
            db.session.commit()
            db.session.delete(position)
            db.session.commit() 
        return redirect(url_for('user_orders',username=username)) 
    return render_template('form_order.html',
                            user=current_user,
                            user_basket = user_basket,
                            total=total,
                            count_position=count_position,
                            form=form_message)


@app.route('/user_profile/<username>/orders/', methods=['GET', 'POST'])
@login_required
def user_orders(username): 
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(desc(Order.time_buy)) 
    return render_template('user_orders.html', username=username, orders=user_orders)


@app.route('/userava/')
@login_required   
def userava():
    img = User.getAvatar(current_user)     
    if not img:
        return ''   
    
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h           



@app.route('/upload/', methods=['GET', 'POST'])
@login_required 
def upload():
    user = User().query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = current_user.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления автара', category='error')
                    return redirect(url_for('user_profile',username=current_user.username))
                flash('Аватар обновлен', category='success')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла', category='error')  
        else:
            flash('Ошибка обновления аватара', category='error')          
    return redirect(url_for('user_profile', username=current_user.username))



@app.route('/user_profile/<username>/change_password/', methods=['GET', 'POST'])
@login_required
def change_password(username):
    username = username
    form = СhangePassword()
    if form.validate_on_submit():
        passw = form.password.data
        new_passw = form.new_password.data
        user = User.query.filter_by(username=username).first() 
        if check_password_hash(user.password, passw):
            hash = generate_password_hash(new_passw)
            user.password = hash
            db.session.commit()
            flag = True
            flash('Пароль успешно сохранен', category='success')
        else:  
            flash('Неверный пароль', category='error')
    return render_template('change_password.html', form=form, username=username)    


@app.route('/user_profile/<username>/logout/')
@login_required
def logout(username):
    logout_user()
    flash("Вы вышли из учетной записи", category='error')
    return redirect(url_for('login'))

    
@app.route('/password_recovery/', methods=['POST', 'GET'])
def password_recovery():
    form_pass_recovery = PasswordRecoveryForm()
    if request.method == 'POST':
        if form_pass_recovery.validate_on_submit():
            user_email = form_pass_recovery.email.data
            u = User()
            user = u.query.filter_by(email=user_email).first()
            if user:
                from passw_recovery import send_email
                temporary_password = send_email(user_email) 
                hash = generate_password_hash(temporary_password)
                user.password  = hash
                db.session.commit()
                flash('Временный пароль отправлен на ваш email', category='success')  
            else:
                flash('Неверный email', category='error') 
        else:       
            flash('Введите корректный email', category='error')    
    return render_template('password_recovery.html', form=form_pass_recovery)


@app.route('/account_recovery/', methods=['POST', 'GET'])
def account_recovery():
    user = None
    form_account_recovery = AccountRecoveryForm()
    if request.method == 'POST':
        if form_account_recovery.validate_on_submit():
            user_email = form_account_recovery.email.data
            u = User()
            user = u.query.filter_by(email=user_email).first()
            if user:
                import secrets
                from account_recovery import send_email
                password = secrets.token_hex(5)
                hash = generate_password_hash(password)
                user.password  = hash 
                user.is_active = True
                context = {'login': user.username, 'password': password}
                send_email(user_email, **context) 
                db.session.commit()
                flash('Инструкция для восстановления учетной записи отправлена на ваш email', category='success')  
            else:
                flash('Неверный email', category='error') 
        else:       
            flash('Введите корректный email', category='error')    
    return render_template('account_recovery.html', form=form_account_recovery, user=user)

    
@app.route('/user_profile/<username>/delete_user_profile/', methods=['POST', 'GET'])
@login_required
def delete_user_profile(username):
    logout_user()
    user = User.query.filter_by(username=username).first()
    user.is_active = False
    db.session.commit()
    return redirect(url_for('registration'))


@app.route('/user_profile/<username>/save_form_account/', methods=['POST', 'GET'])
@login_required
def save_form_account(username):
    user = User.query.filter_by(username=username).first()
    form = UserProfile()
    if request.method == 'POST':
        if form.validate_on_submit():
            user.email = form.email.data
            user.name = form.name.data
            user.age = form.age.data
            user.telephone = form.telephone.data
            user.address = form.address.data     
            db.session.commit()
            flash('Ваши данные обновлены', category='success')
        else:    
            flash('Форма заполнена неккоректно', category='error')
    return render_template('save_form_account.html', form=form, user=user)


@app.route('/user_profile/<username>/orders/', methods=['POST', 'GET'])
@login_required
def orders(username):
    return render_template('orders.html', username=username) 

@app.errorhandler(401)
def pageNotFount(error):
    return render_template('401.html')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('404.html')


@app.errorhandler(500)
def pageNotFount(error):
    return render_template('500.html')


# @app.cli.command("init-db")
# def init_db():
#     db.create_all()
#     print('OK')cls


# user = User_profile.query.filter_by(username='bad1991').first()
# user.username = 'Mark'

# @app.cli.command("add")
# def add():
#     user = UserBasket(user_id=1, 
#                 product_id=2, 
#                 quantity=3, 
#                 price=4, 
#                 )
    
#     db.session.add(user)
#     db.session.commit()
#     print(f'{user.id} add in DB!')

# @app.cli.command("add")
# def add():
#     for i in range(1, 55):
#         new_basket = UserBasket.query.get(i)
#         db.session.delete(new_basket)
#         db.session.commit()           
#     print(f' Deleted in DB!')

# @app.cli.command("edit-john")
# def edit_user():
#     user = User.query.filter_by(username='bad1992').first()
#     user.telephone = '+79821372456'
#     user.address = 'город Волжск ул. Дружбы д.13'
#     user.name = 'Никита'
#     db.session.commit()
#     print('Edit John mail in DB!')


# @app.cli.command("del-user")
# def del_user():
#     user = User.query.filter_by(username='bad1992').first()
#     db.session.delete(user)
#     db.session.commit()
#     print('Delete  from DB!')



if __name__ == '__main__':
    app.run(debug=True)