import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Teachers(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    teacher_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post_id = sqlalchemy.Column(sqlalchemy.ForeignKey("posts.id"))
    way_to_photo = sqlalchemy.Column(sqlalchemy.String, unique=True)
    additional_information = sqlalchemy.Column(sqlalchemy.Text)

    posts = relationship('Posts')
    t_t_s = orm.relationship('Teachers_to_Subjects', back_populates='teacher')


class Posts(SqlAlchemyBase):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    teachers = orm.relationship("Teachers", back_populates='posts')

