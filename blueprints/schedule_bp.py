import flask
from flask import render_template, request, jsonify
from data import db_session
from data.models_all.classes import Classes
from data.models_all.schedule import Schedule
from forms.schedule_form import ScheduleForm

blueprint = flask.Blueprint('schedule_blueprint', __name__, template_folder='templates')


@blueprint.route('/api/schedule')
def schedule_get(data):
    """Получает расписания для одного класса"""
    session = db_session.create_session()
    id_class = session.query(Classes).filter(Classes.grade_level == data.split('_')[0],
                                             Classes.class_word == data.split('_')[1]).first()
    if id_class:
        schedule = session.query(Schedule).filter(Schedule.class_id == id_class.id).all()
        return flask.jsonify(
            {'schedule': [item.to_dict(only=('weekday', 'subject', 'classroom_id')) for item in schedule]})


@blueprint.route('/api/schedule', methods=['POST'])
def schedule_post():
    """Добавляет расписание"""
    form = ScheduleForm(is_editing=True)
    if form.validate_on_submit():
        pass

    return render_template('schedule.html', form=form)
