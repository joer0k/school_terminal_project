import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Schedule(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'schedule'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'), nullable=False)
    day_of_week = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('weekday.id'), nullable=False)

    subject = orm.relationship('Subjects')
    weekday = orm.relationship('Weekday')
