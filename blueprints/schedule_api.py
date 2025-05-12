import flask
from flask import request, jsonify
from sqlalchemy.util import NoneType
from werkzeug.exceptions import BadRequest

from blueprints.canteen_api import change_dish
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


@schedule_bp.route('/parallel/<int:number>', methods=['GET'])
def parallel_get(number):
    '''получает список классов для одной параллели'''
    session = db_session.create_session()
    classes = session.query(Classes).filter(Classes.grade_level == number).all()
    data = {}
    for item in classes:
        if item.grade_level not in data.keys():
            data[item.grade_level] = [item.class_word]
        else:
            data[item.grade_level] += [item.class_word]
    return jsonify(data)


@schedule_bp.route('/schedule', methods=['POST'])
def schedule_post():
    """Добавляет и изменяет расписание"""
    '''смысл работы в том, что в data поступает список вида 
    [{номер урока: 1, предметы для всех дней недели: {}] и так для всех 7-и уроков
    это все обрабатывается, проверяется, что в бд нет такой же записи.
    при наличии удаляет имеющуюся и добавляет заново'''
    session = db_session.create_session()
    data = request.json
    class_id = session.query(Classes).filter(Classes.grade_level == data[-1].split('_')[0],
                                             Classes.class_word == data[-1].split('_')[1]).first().id
    result = []
    for lessons in data[:-1]:  # в result добавляется запись в том виде, в который удобнее добавить в БД
        for day, lesson in lessons['subjects'].items():
            if lesson:
                subject_id = session.query(Subjects).filter(
                    Subjects.subject_name == lesson.split('(')[0].strip()).first()
                if not subject_id:
                    return BadRequest('Ошибка в названии предмета')
                classroom_id = session.query(Classrooms).filter(
                    Classrooms.room_number == lesson.split()[-1].strip(')')).first()
                if not classroom_id:
                    return BadRequest('Ошибка в номере кабинета')
                result += [{'subject_id': subject_id.id, 'classroom': classroom_id.id, 'class_id': class_id,
                            'day_of_week': day, 'number_lesson': lessons['lessonNumber']}]
    try:

        for item in result:  # перебираются записи, уже существующие в БД удаляются и добавляються заново
            schedule = session.query(Schedule).filter(Schedule.class_id == item['class_id'],
                                                      Schedule.classroom_id == item['classroom'],
                                                      Schedule.subject_id == item['subject_id'],
                                                      Schedule.day_of_week == item['day_of_week'],
                                                      Schedule.number_lesson == item['number_lesson']).first()
            if schedule is not None:
                continue
            else:
                result = Schedule(
                    subject_id=item['subject_id'],
                    class_id=item['class_id'],
                    classroom_id=item['classroom'],
                    day_of_week=item['day_of_week'],
                    number_lesson=item['number_lesson'],
                )
                session.add(result)
                session.commit()
        return jsonify({
            'success': 'OK'
        })
    except Exception as error:
        session.rollback()
        raise BadRequest(f'Ошибка: {error}')
    finally:
        session.close()
