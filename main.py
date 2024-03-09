from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from models import db, User_profile, Products, User_basket, LoginUser
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PasswordRecoveryForm
from passw_recovery import send_email


app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


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
            u = User_profile()
            user = u.query.filter_by(username=user_name).first()
            try:
                if user: 
                    flash('Пользователь с таким логином уже существует, придумайте новый', category='error')  
                else:
                    new_user = User_profile(email=email, username=user_name, password=hash)
                    db.session.add(new_user)
                    db.session.commit()

                    user_basket = User_basket(user_id=new_user.id)
                    db.session.add(user_basket)
                    db.session.commit()  
                    flash('Регистрация прошла успешно', category='success')
                    return redirect(url_for('login'))
            except:
                    db.session.rollback()
        else:            
            flash('Данные введены не корректно', category='error')
    return  render_template('registration.html', form=form_registration)    
                   

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'userLogged' in session:
        username=session['userLogged']
        
        
        return redirect(url_for('user_profile', username=session['userLogged']))
     
    form_login = LoginForm()
    if form_login.validate_on_submit():
        u = User_profile()
        user = u.query.filter_by(username=form_login.username.data).first()
        if user and check_password_hash(user.password, form_login.password.data):
            session['userLogged'] = form_login.username.data
            return redirect(url_for('user_profile', username=session['userLogged']))
        else:
            flash('Неверный логин / пароль', category='error')

    return render_template('login.html', form=form_login)    


@app.route('/user_profile/<username>')
def user_profile(username):
    context = {'username': username}
    return render_template('user_profile.html', **context)


    
@app.route('/password_recovery/', methods=['POST', 'GET'])
def password_recovery():
    form_pass_recovery = PasswordRecoveryForm()
    if request.method == 'POST':
        if form_pass_recovery.validate_on_submit():
            user_email = form_pass_recovery.email.data
            u = User_profile()
            user = u.query.filter_by(email=user_email).first()
            if user:
                from passw_recovery import send_email
                temporary_password = send_email(user_email) 
                user.password = generate_password_hash(temporary_password)
                db.session.commit()
                flash('Временный пароль отправлен на ваш email', category='success') 
                return redirect(url_for('login')) 
            else:
                flash('Неверный email', category='error') 
        else:       
            flash('Введите email', category='error')    
    return render_template('password_recovery.html', form=form_pass_recovery)


@app.errorhandler(401)
def pageNotFount(error):
    return render_template('401.html')


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('404.html')


@app.errorhandler(500)
def pageNotFount(error):
    return render_template('500.html')


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("add-user")
def add_user():
    user = User_profile(username='username', password='passw', 
                        email='mail@.com', name=None, age=None)
    
    db.session.add(user)
    db.session.commit()
    print(f'{user.username} add in DB!')


@app.cli.command("edit-john")
def edit_user():
    user = User_profile.query.filter_by(username='john').first()
    user.email = 'new_email@example.com'
    db.session.commit()
    print('Edit John mail in DB!')


@app.cli.command("del")
def del_user():
    user = User_profile.query.filter_by(username='12345@12345').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete John from DB!')
 
    

if __name__ == '__main__':
    app.run(debug=True)