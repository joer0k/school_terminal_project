import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    teacher_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    t_t_s = orm.relationship('Teachers_to_Subjects', back_populates='teacher')
