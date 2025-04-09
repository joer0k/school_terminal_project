import sqlalchemy

from data.schedule.db_schedule import SqlAlchemyBase


class Classrooms(SqlAlchemyBase):
    __tablename__ = 'classrooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    room_number = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))