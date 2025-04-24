import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from data.models_all.menu import MenuTable


class Dishes(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_categories = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id"))
    dish_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    categories = orm.relationship(
        "Categories",
        back_populates="dish"
    )
    dishes = orm.relationship('MenuTable', back_populates="dish")
