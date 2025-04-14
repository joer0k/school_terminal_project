import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.models_all.menu import menu_table

from data.db_session import SqlAlchemyBase


class Weekday(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'weekday'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weekday = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # weekdays = orm.relationship(
    #     "Weekday",
    #     secondary=menu_table,
    #     back_populates="dishes"
    # )
