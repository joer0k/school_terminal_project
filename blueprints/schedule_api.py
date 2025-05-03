import flask
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from data import db_session
from data.models_all.classes import Classes
from data.models_all.classrooms import Classrooms
from data.models_all.schedule import Schedule
from data.models_all.subjects import Subjects

schedule_bp = flask.Blueprint('schedule_api', __name__, template_folder='templates')


@schedule_bp.route('/schedule', methods=['GET'])
def schedule_all_get():
    """Получает расписание для всех классов"""
    session = db_session.create_session()
    schedule = session.query(Schedule).all()
    return flask.jsonify(
        {'schedule': [
            item.to_dict(only=('class_name', 'day_of_week', 'subject.subject_name', 'classroom_id', 'number_lesson'))
            for item
            in
            schedule]})


@schedule_bp.route('/schedule/grade/<int:grade_level>', methods=['GET'])
def schedule_get(grade_level):
    '''Получает расписание для параллели'''
    session = db_session.create_session()
    classes_ids = [classes.id for classes in session.query(Classes).filter(Classes.grade_level == grade_level).all()]
    schedule = session.query(Schedule).filter(Schedule.class_id.in_(classes_ids)).all()
    return flask.jsonify(
        {'schedule': [
            item.to_dict(only=(
                'class_name', 'weekday.weekday', 'subject.subject_name', 'classroom.room_number', 'number_lesson'))
            for item in schedule
        ]}
    )


@schedule_bp.route('/classes', methods=['GET'])
def classes_get():
    '''Получает список всех классов'''
    session = db_session.create_session()
    classes = session.query(Classes).all()
    data = {}
    for item in classes:
        if item.grade_level not in data.keys():
            data[item.grade_level] = [item.class_word]
        else:
            data[item.grade_level] += [item.class_word]
    return jsonify(data)


@schedule_bp.route('/schedule', methods=['POST'])
def schedule_post():
    """Добавляет расписание"""
    session = db_session.create_session()
    data = request.json
    result = []
    class_id = session.query(Classes).filter(Classes.grade_level == data[-1].split('_')[0],
                                             Classes.class_word == data[-1].split('_')[1]).first().id
    result = []
    for lessons in data[:-1]:
        for day, lesson in lessons['subjects'].items():
            if lesson:
                subject_id = session.query(Subjects).filter(Subjects.subject_name == lesson.split()[0]).first().id
                classroom_id = session.query(Classrooms).filter(
                    Classrooms.room_number == lesson.split()[-1].strip(')')).first().id
                result += [{'subject_id': subject_id, 'classroom': classroom_id, 'class_id': class_id,
                           'day_of_week': day, 'number_lesson': lessons['lessonNumber']}]
    required_fields = ['subject_id', 'class_id', 'classroom', 'day_of_week', 'number_lesson']
    if not all(field in data for field in required_fields):
        raise BadRequest('Не все поля заполнены')

    try:
        result = Schedule(
            subject_id=data['subject_id'],
            class_id=data['class_id'],
            classroom_id=data['classroom'],
            day_of_week=data['day_of_week'],
            number_lesson=data['number_lesson'],
        )
        session.add(result)
        session.commit()
        return jsonify({
            'id': result.id,
            'subject_id': result.subject_id,
            'class_id': result.class_id,
            'classroom_id': result.classroom_id,
            'day_of_week': result.day_of_week,
            'number_lesson': result.number_lesson,
        })
    except Exception as error:
        session.rollback()
        raise BadRequest(f'Ошибка: {error}')
    finally:
        session.close()
