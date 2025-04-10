import flask
from flask import render_template, request
from data import db_session
from data.models_all.classes import Classes
from data.models_all.schedule import Schedule

blueprint = flask.Blueprint('schedule_blueprint', __name__, template_folder='templates')


@blueprint.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        session = db_session.create_session()
        id_class = session.query(Classes).filter(Classes.class_word == request.form['class_word'],
                                                 Classes.grade_level == request.form['grade_level']).first().id
        schedule = session.query(Schedule).filter(Schedule.id == id_class).all()

    return render_template('schedule.html')
