import flask
from flask import render_template, request, jsonify
from data import db_session
from data.models_all.classes import Classes
from data.models_all.schedule import Schedule
from forms.schedule_form import ScheduleForm

blueprint = flask.Blueprint('schedule_blueprint', __name__, template_folder='templates')


@blueprint.route('/schedule', methods=['GET', 'POST'])
def schedule_get():
    """Получает расписания для одного класса"""
    form = ScheduleForm(is_editing=False)
    if request.method == 'POST':
        session = db_session.create_session()
        id_class = session.query(Classes).filter(Classes.class_word == request.form['class_word'],
                                                 Classes.grade_level == request.form['grade_level']).first()
        if id_class:
            schedule = session.query(Schedule).filter(Schedule.class_id == id_class.id).all()
            data = {}
            for elem in schedule:
                if elem.weekday.weekday in data.keys():
                    data[elem.weekday.weekday] += [elem.subject.subject_name]
                else:
                    data[elem.weekday.weekday] = [elem.subject.subject_name]
            print(data)
            # в data словарь с предметами для выбранного класса

            # print({'schedule': ([item.to_dict(only=(
            #     'id', 'subject', 'weekday'
            # )) for item in schedule])})
    return render_template('schedule.html', form=form)


@blueprint.route('/add_schedule', methods=['GET', 'PUT'])
def schedule_put():
    """Добавляет расписание"""
    form = ScheduleForm(is_editing=True)
    if form.validate_on_submit():
        pass

    return render_template('schedule.html', form=form)
