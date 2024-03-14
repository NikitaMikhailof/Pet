from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
csrf = CSRFProtect(app)

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Проверка пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class PasswordRecoveryForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Отправить')
  

class СhangePassword(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('Новый пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Сохранить')
