from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    '''Форма входа'''
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=20)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
