import flask
from flask import session, request, jsonify
from werkzeug.exceptions import BadRequest, Conflict, NotFound

from data import db_session
from data.models_all.users import User

users_bp = flask.Blueprint('users_api', __name__, template_folder='templates')


@users_bp.route('/users', methods=['GET'])
def get_users():
    '''Возвращает данные о всех пользователях'''
    session = db_session.create_session()
    users = session.query(User).all()
    return flask.jsonify(
        {'users': (
            [item.to_dict(only=('id', 'surname', 'name', 'email')) for item in
             users])})


@users_bp.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user):
    '''Возвращает данные об одном пользователе'''
    print(1)
    session = db_session.create_session()
    user = session.query(User).get(id_user)
    if user:
        return flask.jsonify({'users': ([user.to_dict(
            only=('id', 'surname', 'name', 'email')
        )])})
    return flask.abort(404)


@users_bp.route('/user/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    '''Удаляет пользователя'''
    session = db_session.create_session()
    user = session.get(User, id_user)
    if user:
        session.delete(user)
        session.commit()
        return flask.jsonify({'status': 'Успешно'}), 202
    else:
        session.close()
        flask.abort(404)


@users_bp.route('/users', methods=['POST'])
def create_user():
    '''Создает аккаунт пользователя'''
    data = request.get_json()

    required_fields = ['surname', 'name', 'email', 'password', 'repeat_password']
    if not all(field in data for field in required_fields):
        raise BadRequest('Заполните все необходимые поля')
    session = db_session.create_session()
    if data['password'] != data['repeat_password']:
        raise Conflict('Пароли не совпадают')
    if session.get(User, data['email']):
        raise Conflict('Пользователь с таким email уже существует')
    try:
        user = User(
            surname=data['surname'],
            name=data['name'],
            email=data['email'],
        )
        user.set_password(data['password'])
        session.add(user)
        session.commit()
        return jsonify({
            'id': user.id,
            'surname': user.surname,
            'name': user.name,
            'email': user.email,
        }), 200
    except Exception as error:
        session.rollback()
        raise BadRequest(str(error))
    finally:
        session.close()


@users_bp.route('/user/<int:id_user>', methods=['PUT'])
def change_user(id_user):
    '''Изменяет данные аккаунта пользователя'''
    data = request.get_json()
    required_fields = ['id', 'surname', 'name', 'email']
    session = db_session.create_session()
    try:
        user = session.get(User, id_user)
        if not user:
            raise NotFound('Пользователь не найден')
        for field in required_fields:
            if field in data:
                setattr(user, field, data[field])
        if 'password' in data or 'repeat_password' in data:
            if data['password'] != data['repeat_password']:
                raise Conflict('Пароли не совпадают')
            user.set_password(data['password'])
        session.commit()
        return jsonify({
            'id': user.id,
            'surname': user.surname,
            'name': user.name,
            'email': user.email,
        }), 200
    except Exception as error:
        session.rollback()
        raise BadRequest(str(error))
    finally:
        session.close()
