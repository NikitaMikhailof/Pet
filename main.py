from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from models import db, User_profile, Products, User_basket
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from flask_login import LoginManager



app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/login/', methods=['GET', 'POST'])
def login():
    pass
    form = LoginForm()
    if request.method == 'POST' and form.validate():
    # Обработка данных из формы
        pass
    return render_template('login.html', form=form)


@app.route('/user_profile/<username>')
def user_profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'Профиль пользователя {username}'


@app.route('/registration/', methods=['POST', 'GET'])
def registration():    
    if request.method == 'POST':
        if '@' in request.form['email'] and len(request.form['username']) > 4 \
            and len(request.form['password']) > 6:
            try:
                hash = generate_password_hash(request.form['password'])
                mail = request.form['email']
                user_name = request.form['username']
                new_user = User_profile(email=mail, username=user_name, password=hash)
                db.session.add(new_user)
                db.session.commit()

                user_basket = User_basket(user_id=new_user.id)
                db.session.add(user_basket)
                db.session.commit()
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                print('Ошибка добавления в базу данных')
        else:
            flash('неверно заполнены поля', category='error')    
    return  render_template('registration.html')             



@app.route('/password_recovery/')
def password_recovery():
    if request.method == 'POST':
        print(request.form)
    return render_template('password_recovery.html')


@app.route('/send_password_email/')
def send_password_email():
    return render_template('send_password_email.html')


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
          

if __name__ == '__main__':
    app.run(debug=True)