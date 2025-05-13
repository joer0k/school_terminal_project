import flask
from flask import request, make_response, jsonify

from data import db_session
from data.models_all.dishes import Dishes
from data.models_all.weekday import Weekday

canteen_bp = flask.Blueprint(
    'canteen_api',
    __name__,
    template_folder='templates'
)


# Получение меню на неделю
@canteen_bp.route('/menu')
def get_week_menu():
    with db_session.create_session() as session:
        weekdays = session.query(Weekday).all()
        result = [
            {
                "id": weekday.id,
                "weekday": weekday.weekday,
                "dishes": [
                    {
                        "id": dish.id,
                        "title": dish.dish_name,
                        "img": dish.image,
                        "desc": dish.description,
                        "category": weekday.weekday.upper()

                    }
                    for dish in weekday.menu_items
                ]
            }
            for weekday in weekdays
        ]
        return jsonify({"menu": result})


# Меню на день недели
@canteen_bp.route('/menu/<int:weekday_id>')
def get_weekday_menu(weekday_id):
    with db_session.create_session() as session:
        weekday = session.query(Weekday).filter_by(id=weekday_id).first()
        if weekday:
            result = [
                {
                    "id": dish.id,
                    "dish_name": dish.dish_name,
                    "image": dish.image,
                    "description": dish.description,
                    "category": dish.categories.dish_category,
                    "weekday": weekday.weekday
                }
                for dish in weekday.menu_items
            ]
            return jsonify({"menu": result})
        return jsonify({"menu": 'Не составлено!'})


@canteen_bp.route('/dishes', methods=['GET'])
def get_dishes():
    with db_session.create_session() as session:
        dishes = session.query(Dishes).all()
        if dishes:
            result = [
                {
                    "id": dish.id,
                    "dish_name": dish.dish_name,
                    "image": dish.image,
                    "description": dish.description,
                    "category": dish.categories.dish_category
                }
                for dish in dishes
            ]
            return jsonify({"dishes": result})
        return jsonify({"dishes": "Не найдено!"})


@canteen_bp.route('/dishes/<int:dish_id>', methods=['GET'])
def get_dishes_by_id(dish_id):
    with db_session.create_session() as session:
        dish = session.query(Dishes).filter_by(id=dish_id).first()
        if dish:
            result = [
                {
                    "id": dish.id,
                    "dish_name": dish.dish_name,
                    "image": dish.image,
                    "description": dish.description
                }
            ]
            return jsonify({"dishes": result})
        return jsonify({"dishes": "Не найдено!"})


@canteen_bp.route('/dishes/category/<int:category_id>', methods=['GET'])
def get_dishes_by_category(category_id):
    with db_session.create_session() as session:
        dishes = session.query(Dishes).filter_by(id_categories=category_id).all()
        if dishes:
            result = [
                {
                    "id": dish.id,
                    "dish_name": dish.dish_name,
                    "image": dish.image,
                    "description": dish.description
                }
                for dish in dishes
            ]
            return jsonify({"dishes": result})
        return jsonify({"dishes": "Не найдено!"})


@canteen_bp.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    with db_session.create_session() as session:
        dish = session.query(Dishes).get(dish_id)

        if not dish:
            return make_response(jsonify({'error': 'Not found'}), 404)
        session.delete(dish)
        session.commit()
        return jsonify({'success': 'OK'})


@canteen_bp.route('/dishes/<int:dish_id>', methods=['PUT'])
def change_dish(dish_id):
    with db_session.create_session() as session:
        dish = session.query(Dishes).get(dish_id)
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
        session.commit()
        return jsonify({'id': dish.id})
