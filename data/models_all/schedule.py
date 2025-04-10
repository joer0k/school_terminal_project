import sqlalchemy

from data.db_session import SqlAlchemyBase


class Schedule(SqlAlchemyBase):
    __tablename__ = 'schedule'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=False)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('classes.id'), nullable=False)
    day_of_week = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('weekday.id'), nullable=False)

