import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Subjects(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'), nullable=False)

    class_number = orm.relationship('Classes')
    class_room = orm.relationship('Classrooms')
    t_t_s = orm.relationship('Teachers_to_Subjects', back_populates='subject')
