import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Teachers_to_Subjects(SqlAlchemyBase):
    __tablename__ = 'teacher_to_subject'

    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=False)

    # teacher = orm.relationship('Teachers', backref='t_t_s')
    # subject = orm.relationship('Subjects')
