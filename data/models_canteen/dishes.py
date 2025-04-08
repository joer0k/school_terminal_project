import sqlalchemy
from sqlalchemy import orm
from data.models_canteen.menu import menu_table

from data.db_canteen import SqlAlchemyBase


class Dishes(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_categories = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    dish_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=True)


    dishes = orm.relationship(
        "Dishes",
        secondary=menu_table,
        back_populates="weekdays"
    )