import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Schedule(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'schedule'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'), nullable=False)
    classroom_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classrooms.id'), nullable=False)
    day_of_week = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('weekday.id'), nullable=False)
    number_lesson = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    subject = orm.relationship('Subjects')
    weekday = orm.relationship('Weekday')
    class_name = orm.relationship('Classes')
