import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase

dish_to_weekday = sqlalchemy.Table(
    'dish_to_weekday',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('dishes', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('dishes.id')),
    sqlalchemy.Column('weekday', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('weekday.id'))
)


class Dishes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_categories = sqlalchemy.Column(sqlalchemy.ForeignKey("categories.id"))
    dish_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=True, default='data/static/images/default.jpg')
    description = sqlalchemy.Column(sqlalchemy.Text, default='Не указано')

    categories = orm.relationship("Categories", back_populates="dish")
    weekdays = orm.relationship("data.models_all.weekday.Weekday", secondary='dish_to_weekday', back_populates="menu_items")
