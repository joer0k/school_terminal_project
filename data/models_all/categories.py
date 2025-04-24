import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    dish_category = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    dish = orm.relationship('Dishes', back_populates='categories')
