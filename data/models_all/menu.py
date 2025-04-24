from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.util.preloaded import orm

from data.db_session import SqlAlchemyBase


class MenuTable(SqlAlchemyBase):
    __tablename__ = 'menu_table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_weekday = Column(Integer, ForeignKey('weekday.id'), nullable=False)
    id_dish = Column(Integer, ForeignKey('dishes.id'), nullable=False)

    weekday = orm.relationship("Weekday", back_populates="menu_items")
    dish = orm.relationship("Dishes", back_populates="dishes")
