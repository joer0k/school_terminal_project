import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Classes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_word = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    grade_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
