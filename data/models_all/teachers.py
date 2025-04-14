import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Teachers(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    teacher_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    way_to_photo = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    additional_information = sqlalchemy.Column(sqlalchemy.Text)
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'))
    posts = orm.relationship("Posts")
    # t_t_s = orm.relationship('Teachers_to_Subjects', back_populates='teacher')


class Posts(SqlAlchemyBase):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    teacher = orm.relationship("Teachers", back_populates='posts')
