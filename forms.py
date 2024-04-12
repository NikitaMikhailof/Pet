from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, InputRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = '4470a67a983583b8d6287e88b4f25ca5bf212514b0add95fde48a5e6abbd6dd0'
csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


# class AdminForm(LoginForm):
#     pass


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

class UserProfile(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, message='Введите корректное имя')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50, message='Введите корректный email')])
    telephone = StringField('Телефон', validators=[InputRequired(message='Введите корректный номер'), Length(min=11)])
    age = IntegerField('Возраст', validators=[NumberRange(min=14, max=100)])
    address = StringField('Адрес доставки', validators=[InputRequired(), Length(max=100)])
    submit = SubmitField('Сохранить')


COUNT_PRODUCTS = [('1', 1),
                  ('2', 2),
                  ('3', 3),
                  ('4', 4),
                  ('5', 5),
                  ('6', 6),
                  ('7', 7),
                  ('8', 8),
                  ('9', 9),
                  ('10', 10),
                  ]

class Basket(FlaskForm):
    count = SelectField(choices=COUNT_PRODUCTS, default=1)
    title = StringField()
    submit = SubmitField('В корзину')


class BasketPositionDelete(FlaskForm):
    title = StringField()
    submit = SubmitField('Удалить из корзины')


TYPE_PAYMENT = [('наличными', 'наличными'),
                  ('картой', 'картой'),
                  ('переводом', 'переводом'),
                  ]

class MessageOrder(FlaskForm):
    type_payment = SelectField('способ оплаты', choices=TYPE_PAYMENT, default='переводом')
    message = StringField()
    submit = SubmitField('Заказать')
    

class AccountRecoveryForm(PasswordRecoveryForm):   
    pass


