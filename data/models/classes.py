import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_word = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    grade_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    subjects = orm.relationship('Subjects', back_populates='class_')
