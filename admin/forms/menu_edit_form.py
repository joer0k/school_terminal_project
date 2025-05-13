from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.models_all.categories import Categories
from data.models_all.dishes import Dishes


class MenuEditForm(FlaskForm):
    """Форма добавлению нового блюда"""
    weekday = StringField('', validators=[DataRequired()])
    first_dish_1 = SelectField('', validators=[DataRequired()])
    first_dish_2 = SelectField('', validators=[DataRequired()])
    first_dish_3 = SelectField('', validators=[DataRequired()])
    first_dish_4 = SelectField('', validators=[DataRequired()])
    second_dish_1 = SelectField('', validators=[DataRequired()])
    second_dish_2 = SelectField('', validators=[DataRequired()])
    second_dish_3 = SelectField('', validators=[DataRequired()])
    second_dish_4 = SelectField('', validators=[DataRequired()])
    drinks_1 = SelectField('', validators=[DataRequired()])
    drinks_2 = SelectField('', validators=[DataRequired()])
    drinks_3 = SelectField('', validators=[DataRequired()])
    drinks_4 = SelectField('', validators=[DataRequired()])

    submit = SubmitField('Сохранить')

    def __init__(self, *args, is_editing=False, day=None, **kwargs):
        super(MenuEditForm, self).__init__(*args, **kwargs)
        with db_session.create_session() as session:
            dishes = session.query(Dishes).all()
            dishes_name = sorted([(dish.dish_name, dish.id_categories) for dish in dishes], key=lambda x: (x[1], x))
            categories = session.query(Categories).all()
            categories_id = [(category.dish_category, category.id) for category in categories]
            category_1 = [cat[1] for cat in categories_id if cat[0] == "Первые блюда"][0]
            category_2 = [cat[1] for cat in categories_id if cat[0] == "Вторые блюда"][0]
            category_3 = [cat[1] for cat in categories_id if cat[0] == "Напитки"][0]
            first_block = [self.first_dish_1, self.first_dish_2,
                           self.first_dish_3, self.first_dish_4]
            for item in first_block:
                item.choices = ['-- Отсутствует --']
                item.choices += [dish[0] for dish in dishes_name if dish[1] == category_1]
            second_block = [self.second_dish_1, self.second_dish_2,
                            self.second_dish_3, self.second_dish_4]
            for item in second_block:
                item.choices = ['-- Отсутствует --']
                item.choices += [dish[0] for dish in dishes_name if dish[1] == category_2]
            drink_block = [self.drinks_2, self.drinks_3, self.drinks_4, self.drinks_1]
            for item in drink_block:
                item.choices = ['-- Отсутствует --']
                item.choices += [dish[0] for dish in dishes_name if dish[1] == category_3]

            if is_editing and day:
                day_menu = [(item.dish_name, item.categories.dish_category) for item in day.menu_items]
                first_dishes = [name for name, category in day_menu if category == "Первые блюда"]
                second_dishes = [name for name, category in day_menu if category == "Вторые блюда"]
                drinks = [name for name, category in day_menu if category == "Напитки"]
                for category in [first_dishes, second_dishes, drinks]:
                    while len(category) < 4:
                        category.append('-- Отсутствует --')
                print(first_dishes, second_dishes, drinks)
                # Первые блюда
                self.first_dish_1.data = first_dishes[0]
                self.first_dish_2.data = first_dishes[1]
                self.first_dish_3.data = first_dishes[2]
                self.first_dish_4.data = first_dishes[3]

                # Вторые блюда
                self.second_dish_1.data = second_dishes[0]
                self.second_dish_2.data = second_dishes[1]
                self.second_dish_3.data = second_dishes[2]
                self.second_dish_4.data = second_dishes[3]

                # Напитки
                self.drinks_1.data = drinks[0]
                self.drinks_2.data = drinks[1]
                self.drinks_3.data = drinks[2]
                self.drinks_4.data = drinks[3]
