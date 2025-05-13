import flask
from flask import request, make_response, jsonify

from data import db_session
from data.models_all.teachers import Posts

posts_blueprint = flask.Blueprint(
    'posts_api',
    __name__,
    template_folder='templates'
)


@posts_blueprint.route('/posts')
def get_posts():
    with db_session.create_session() as session:
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
    with db_session.create_session() as session:

        new_post = Posts(
            title=post['title'],
            post=post['post']
        )
        session.add(new_post)
        session.commit()
        return jsonify({'id': new_post.id})


@posts_blueprint.route('/posts/<int:post_id>')
def get_one_post(post_id):
    with db_session.create_session() as session:
        post = session.query(Posts).get(post_id)
        return flask.jsonify({'post': post.to_dict(
            only=('id', 'title', 'post'))})


@posts_blueprint.route('/posts/exactly/<post>')
def get_exactly_post(post):
    with db_session.create_session() as session:
        exactly_post = session.query(Posts).filter(Posts.post == post).all()
        for i in exactly_post:
            print(i)
        return exactly_post


@posts_blueprint.route('/posts/<int:post_id>', methods=['PUT'])
def change_post(post_id):
    with db_session.create_session() as session:

        post = session.query(Posts).get(post_id)
        different = request.json

        if not post:
            return make_response(jsonify({'error': 'Bad request'}), 400)
        elif not any(key in different for key in
                     ['title', 'post']):
            return make_response(jsonify({'error': 'Bad request'}), 400)

        post.title = different['title'] if 'title' in different else post.title
        post.post = different['post'] if 'post' in different else post.post
        session.commit()
        return jsonify({'id': post.id})
