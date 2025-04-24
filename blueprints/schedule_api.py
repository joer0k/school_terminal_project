import flask
from flask import render_template, request, jsonify
from data import db_session
from data.models_all.classes import Classes
from data.models_all.schedule import Schedule
from forms.schedule_form import ScheduleForm

schedule_bp = flask.Blueprint('schedule_api', __name__, template_folder='templates')
'''
Доделаю апи когда будет готов примерный вид изменения\добавления расписания
Потому что я хочу изменять и добавлять предметы, записывая в таблицу, а сейчас это сложно т.к. не 
знаю как это будет выглядеть.
'''


@schedule_bp.route('/schedule')
def schedule_get(data):
    """Получает расписания для одного класса"""
    session = db_session.create_session()
    id_class = session.query(Classes).filter(Classes.grade_level == data.split('_')[0],
                                             Classes.class_word == data.split('_')[1]).first()
    if id_class:
        schedule = session.query(Schedule).filter(Schedule.class_id == id_class.id).all()
        return flask.jsonify(
            {'schedule': [
                item.to_dict(only=('day_of_week', 'subject.subject_name', 'classroom_id', 'number_lesson')) for item
                in
                schedule]})


@schedule_bp.route('/schedule', methods=['POST'])
def schedule_post():
    """Добавляет расписание"""
    form = ScheduleForm(is_editing=True)
    if form.validate_on_submit():
        pass

    return render_template('schedule.html', form=form)
