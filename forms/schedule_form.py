from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    """Вспомогательная форма для одного предмета"""
    subject = StringField('Предмет')


class DayScheduleForm(FlaskForm):
    """Вспомогательная форма для одного дня"""
    lessons = FieldList(FormField(LessonForm), min_entries=7, max_entries=7)  # 7 уроков


class ScheduleForm(FlaskForm):
    """Форма всего расписания"""
    grade_level = SelectField('Класс', choices=[(str(i), str(i)) for i in range(5, 12)], default='',
                              validators=[DataRequired()])
    class_word = SelectField('Буква класса', choices=[(i, i) for i in ('АБВГД')], default='',
                             validators=[DataRequired()])
    is_edit = BooleanField("Редактирование")
    days = FieldList(FormField(DayScheduleForm), min_entries=6, max_entries=6)  # 6 дней недели

    submit = SubmitField('Показать')
