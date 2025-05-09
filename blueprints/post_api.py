import flask
from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash

from data import db_session
from data.models_all.teachers import Teachers, Posts

posts_blueprint = flask.Blueprint(
    'posts_api',
    __name__,
    template_folder='templates'
)


@posts_blueprint.route('/posts')
def get_posts():
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    teachers = session.query(Posts).all()
    return flask.jsonify({'posts': [item.to_dict(
        only=('id', 'title', 'post')) for
        item in teachers]})


@posts_blueprint.route('/posts', methods=['POST'])
def create_post():
    post = request.json
    if not post:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in post for key in
                 ['title', 'post']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    new_post = Posts(
        title=post['title'],
        post=post['post']
    )
    db_sess.add(new_post)
    db_sess.commit()
    return jsonify({'id': new_post.id})

@posts_blueprint.route('/posts/<int:post_id>')
def get_one_post(post_id):
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    post = session.query(Posts).get(post_id)
    return flask.jsonify({'post': post.to_dict(
        only=('id', 'title', 'post'))})


@posts_blueprint.route('/posts/exactly/<post>')
def get_exactly_post(post):
    db_session.global_init("db/information.db")
    session = db_session.create_session()
    exactly_post = session.query(Posts).filter(Posts.post == post).all()
    for i in exactly_post:
        print(i)
    return exactly_post


@posts_blueprint.route('/posts/<int:post_id>', methods=['PUT'])
def change_post(post_id):
    db_session.global_init("db/information.db")
    db_sess = db_session.create_session()
    post = db_sess.query(Posts).get(post_id)
    different = request.json

    if not post:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    elif not any(key in different for key in
                 ['title', 'post']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    post.title = different['title'] if 'title' in different else post.title
    post.post = different['post'] if 'post' in different else post.post
    db_sess.commit()
    return jsonify({'id': post.id})

