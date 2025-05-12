from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

from data import db_session
from data.models_all.categories import Categories


class AddDishForm(FlaskForm):
    """Форма добавлению нового блюда"""

    categories = SelectField('Категория', validators=[DataRequired()])
    dish_name = StringField('Название', validators=[DataRequired()])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    description = TextAreaField('Описание')

    submit = SubmitField('Сохранить')

    def __init__(self, *args, is_editing=False, **kwargs):
        super(AddDishForm, self).__init__(*args, **kwargs)
        session = db_session.create_session()
        self.categories.choices = [elem.dish_category for elem in session.query(Categories).all()]

