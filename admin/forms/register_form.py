from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, optional, Length

from data import db_session
from data.models_all.teachers import Posts


class RegisterForm(FlaskForm):
    '''Форма регистрации'''
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    second_name = StringField('Отчество')
    date_bd = DateField('Дата рождения', validators=[DataRequired()])
    speciality = SelectField('Должность', validators=[DataRequired()], choices=[])
    submit = SubmitField('Зарегистрироваться')

    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[optional(), Length(min=8, max=20)])
    password_repeat = PasswordField('Повторите пароль', validators=[optional(), Length(min=8, max=20)])

    def __init__(self, *args, is_editing=False, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.is_editing = is_editing
        with db_session.create_session() as session:

            self.speciality.choices = [elem.title for elem in session.query(Posts).all()]
            if not self.is_editing:
                self.password.validators = [DataRequired(), Length(min=8, max=20)]
                self.password_repeat.validators = [DataRequired(), Length(min=8, max=20)]
                self.submit.label.text = 'Зарегистрироваться'
            else:
                self.submit.label.text = 'Подтвердить изменения'
