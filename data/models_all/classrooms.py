import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Classrooms(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classrooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    room_number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))

    subject = orm.relationship('Subjects')
    teacher = orm.relationship('Teachers')
