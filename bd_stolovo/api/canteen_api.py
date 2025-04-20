import flask
from flask import request, make_response, jsonify

from bd_stolovo.data import db_session
from bd_stolovo.data.models.dishes import Dishes
from bd_stolovo.data.models.menu import MenuTable
from bd_stolovo.data.models.weekday import Weekday

canteen_blueprint = flask.Blueprint(
    'canteen_api',
    __name__,
    template_folder='templates'
)


@canteen_blueprint.route('/canteen')
def get_weekday():
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    weekday = session.query(Weekday).all()
    return flask.jsonify({'weekday': [item.to_dict(
        only=('id', 'weekday')) for item in weekday]})


@canteen_blueprint.route('/canteen/<int:weekday_id>')
def get_menu(weekday_id):
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    canteen = session.query(MenuTable).get(weekday_id)
    return flask.jsonify({'menu': [canteen.to_dict(
        only='id_dish')]})


@canteen_blueprint.route('/dishes', methods=['POST'])
def create_dish():
    dish = request.json
    if not dish:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in dish for key in
                 ['id', 'id_categories', 'dish_name', 'image']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    new_dish = Dishes(
        id=dish['id'],
        id_categories=dish['id_categories'],
        dish_name=dish['dish_name'],
        image=dish['image'],
    )
    db_sess.add(new_dish)
    db_sess.commit()
    return jsonify({'id': new_dish.id})


@canteen_blueprint.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    db_sess = db_session.create_session()
    dish = db_sess.query(Dishes).get(dish_id)
    if not dish:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(dish)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@canteen_blueprint.route('/canteen/<int:menu_id>', methods=['DELETE'])
def delete_menu_on_day(menu_id):
    db_sess = db_session.create_session()
    menu = db_sess.query(MenuTable).get(menu_id)
    if not menu:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(menu)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@canteen_blueprint.route('/teachers/<int:menu_id>', methods=['PUT'])
def change_user(menu_id):
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    menu_on_day = db_sess.query(MenuTable).get(menu_id)
    different = request.json

    if not menu_on_day:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not any(key in different for key in
                 ['id_weekday', 'id_dish']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    menu_on_day.id_weekday = different['id_weekday'] if 'id_weekday' in different else menu_on_day.id_weekday
    menu_on_day.id_dish = different['id_dish'] if 'id_dish' in different else menu_on_day.id_dish
    db_sess.commit()
    return jsonify({'id': menu_on_day.id})


@canteen_blueprint.route('/teachers/<int:dish_id>', methods=['PUT'])
def change_user(dish_id):
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    dish = db_sess.query(Dishes).get(dish_id)
    different = request.json

    if not dish:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not any(key in different for key in
                 ['id', 'id_categories', 'dish_name', 'image']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    dish.id = different['id'] if 'id' in different else dish.id
    dish.id_categories = different['id_categories'] if 'id_categories' in different else dish.id_categories
    dish.dish_name = different['dish_name'] if 'dish_name' in different else dish.dish_name
    dish.image = different['image'] if 'image' in different else dish.image
    db_sess.commit()
    return jsonify({'id': dish.id})
