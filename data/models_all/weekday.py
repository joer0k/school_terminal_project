import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class Weekday(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'weekday'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weekday = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    menu_items = orm.relationship(
        "Dishes",
        secondary='dish_to_weekday',
        back_populates="weekdays"
    )
