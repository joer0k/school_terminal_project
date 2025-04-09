from sqlalchemy import Table, Column, Integer, ForeignKey

from data.canteen.db_canteen import SqlAlchemyBase

menu_table = Table(
    'menu_table', SqlAlchemyBase.metadata,
    Column('id_weekday', Integer, ForeignKey('weekday.id'), primary_key=True),
    Column('id_dish', Integer, ForeignKey('dishes.id'), primary_key=True)
)