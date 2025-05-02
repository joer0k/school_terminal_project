import flask
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

from data import db_session
from data.models_all.classes import Classes
from data.models_all.schedule import Schedule

schedule_bp = flask.Blueprint('schedule_api', __name__, template_folder='templates')


@schedule_bp.route('/schedule', methods=['GET'])
def schedule_get():
    """Получает расписание для всех классов"""
    session = db_session.create_session()
    schedule = session.query(Schedule).all()
    return flask.jsonify(
        {'schedule': [
            item.to_dict(only=('class_name', 'day_of_week', 'subject.subject_name', 'classroom_id', 'number_lesson'))
            for item
            in
            schedule]})
    # data = []
    # for item in schedule:
    #     data += {'schedule': [
    #         f'{item.class_name.class_word}_{item.class_name.grade_level}',
    #         item.day_of_week,
    #         item.subject.subject_name,
    #         item.classroom_id,
    #         item.number_lesson
    #     ]}
    # return jsonify(data)


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
