from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

from data import db_session
from data.models_all.categories import Categories
from data.models_all.teachers import Posts


class AddTeacherForm(FlaskForm):
    """Форма добавлению нового учителя"""

    post = SelectField('Должность', validators=[DataRequired()])
    teacher_name = StringField('ФИО', validators=[DataRequired()])
    photo = FileField('Фото', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    additional_information = TextAreaField('Дополнительная информация')

    submit = SubmitField('Сохранить')

    def __init__(self, *args, is_editing=False, **kwargs):
        super(AddTeacherForm, self).__init__(*args, **kwargs)
        session = db_session.create_session()
        self.post.choices = [elem.title for elem in session.query(Posts).all()]

