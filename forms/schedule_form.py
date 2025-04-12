from random import choices

from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField
from wtforms.fields.choices import SelectField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Optional


# вспомогательная форма для предмета
class LessonForm(FlaskForm):
    subject = StringField('Предмет')


# Вспомогательная форма для одного дня
class DayScheduleForm(FlaskForm):
    lessons = FieldList(FormField(LessonForm), min_entries=7, max_entries=7)  # 7 уроков


# форма всего расписания
class ScheduleForm(FlaskForm):
    grade_level = SelectField('Класс', choices=[(str(i), str(i)) for i in range(1, 12)], validators=[DataRequired()])
    class_word = SelectField('Буква класса', choices=[(i, i) for i in ('АБВГД')], validators=[DataRequired()])

    days = FieldList(FormField(DayScheduleForm), min_entries=6, max_entries=6, validators=[Optional()])  # 6 дней недели

    submit = SubmitField('Сохранить')

    def __init__(self, *args, is_editing=False, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.is_editing = is_editing

        if not self.is_editing:
            self.days.validators = [DataRequired()]
            self.submit.label.text = 'Показать'
        else:
            self.submit.label.text = 'Сохранить'
