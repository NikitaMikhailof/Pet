from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from models import db, User, Products, Order
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PasswordRecoveryForm, СhangePassword, AccountRecoveryForm
from passw_recovery import send_email
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html') 


 
@app.route('/registration/', methods=['POST', 'GET'])
def registration():  
    form_registration = RegistrationForm() 
    if request.method == 'POST': 
        if form_registration.validate_on_submit():
            email = form_registration.email.data
            user_name = form_registration.username.data
            hash = generate_password_hash(form_registration.password.data)
            u = User()
            user = u.query.filter_by(username=user_name).first()
            try:
                if user: 
                    flash('Пользователь с таким логином уже существует, придумайте новый', category='error')  
                else:
                    new_user = User(email=email, username=user_name, password=hash)
                    db.session.add(new_user)
                    db.session.commit()

                    user_basket = Order(user_id=new_user.id)
                    db.session.add(user_basket)
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
        flash("Неверный логин / пароль", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)
            

@app.route('/user_profile/<username>')
@login_required
def user_profile(username): 
    user = User.query.filter_by(username='bad1992').first()
    context = {'username': user.username,
               'email': user.email,
               'telephone': user.telephone,
               'name': user.name,
               'age': user.age,
               'address': user.address,
               'is_active': user.is_active}
    return render_template('user_profile.html', **context)



@app.route('/user_profile/<username>/change_password', methods=['GET', 'POST'])
def change_password(username):
    flag = False
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
    return render_template('change_password.html', form=form, username=username, flag=flag)    


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из учетной записи", category='error')
    return redirect(url_for('login'))

    
@app.route('/password_recovery/', methods=['POST', 'GET'])
def password_recovery():
    user = None
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
    return render_template('password_recovery.html', form=form_pass_recovery, user=user)


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
def delete_user_profile(username):
    logout_user()
    u = User()
    user = u.query.filter_by(username=username).first()
    user.is_active = False
    db.session.commit()
    return redirect(url_for('registration'))


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
#     print('OK')

# user = User_profile.query.filter_by(username='bad1991').first()
# user.username = 'Mark'

# @app.cli.command("add")
# def add():
#     user = User(username='bad1992', 
#                 password='bad1992', 
#                 email='mikhailoffnikita2016@yandex.ru', 
#                 name='Никита', 
#                 age=31,
#                 telephone='+79821372456',
#                 address = 'город Волжск ул. Дружбы д.13')
    
#     db.session.add(user)
#     db.session.commit()
#     print(f'{user.username} add in DB!')


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