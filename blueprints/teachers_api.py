import flask
import requests
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash

from data import db_session
from data.models_all.teachers import Teachers

teachers_blueprint = flask.Blueprint(
    'teachers_api',
    __name__,
    template_folder='templates'
)


@teachers_blueprint.route('/teachers')
def get_teachers():
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    teachers = session.query(Teachers).all()
    return flask.jsonify({'teachers': [item.to_dict(
        only=('id', 'teacher_name', 'post_id', 'way_to_photo', 'additional_information')) for
        item in teachers]})


@teachers_blueprint.route('/teachers/<int:teacher_id>')
def get_one_teacher(teacher_id):
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    teacher = session.query(Teachers).get(teacher_id)
    return flask.jsonify({'teacher': [teacher.to_dict(
        only=('id', 'teacher_name', 'post_id', 'way_to_photo', 'additional_information'))]})


@teachers_blueprint.route('/teachers', methods=['POST'])
def create_teacher():
    teacher = request.json
    if not teacher:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in teacher for key in
                 ['teacher_name', 'post_id', 'way_to_photo', 'additional_information']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    new_teacher = Teachers(
        teacher_name=teacher['teacher_name'],
        post_id=teacher['post_id'],
        way_to_photo=teacher['way_to_photo'],
        additional_information=teacher['additional_information'],
    )
    db_sess.add(new_teacher)
    db_sess.commit()
    return jsonify({'id': new_teacher.id})


@teachers_blueprint.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_user(teacher_id):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teachers).get(teacher_id)
    if not teacher:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(teacher)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@teachers_blueprint.route('/teachers/<int:teacher_id>', methods=['PUT'])
def change_user(teacher_id):
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teachers).get(teacher_id)
    different = request.json

    if not teacher:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not any(key in different for key in
                 ['teacher_name', 'post_id', 'way_to_photo', 'additional_information']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    teacher.teacher_name = different['teacher_name'] if 'teacher_name' in different else teacher.teacher_name
    teacher.post_id = different['post_id'] if 'post_id' in different else teacher.post_id
    teacher.way_to_photo = different['way_to_photo'] if 'way_to_photo' in different else teacher.way_to_photo
    teacher.additional_information = different[
        'additional_information'] if 'additional_information' in different else teacher.additional_information
    db_sess.commit()
    return jsonify({'id': teacher.id})
