import sqlalchemy
from sqlalchemy import orm
from bd_stolovo.data.models.menu import menu_table


from ..db_session import SqlAlchemyBase


class Weekday(SqlAlchemyBase):
    __tablename__ = 'weekday'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weekday = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    weekdays = orm.relationship(
        "Weekday",
        secondary=menu_table,
        back_populates="dishes"
    )
