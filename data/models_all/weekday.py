import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase
from data.models_all.menu import MenuTable


class Weekday(SqlAlchemyBase):
    __tablename__ = 'weekday'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weekday = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    menu_items = orm.relationship(
        "MenuTable", back_populates="weekday"
    )
