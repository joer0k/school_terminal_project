from flask import Flask, render_template, request

import blueprints.schedule_bp
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
@app.route('/index')
def index():
    '''Прогружает главную страницу'''
    return render_template('main.html')


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    # app.register_blueprint(blueprints.schedule_bp.blueprint)
    # app.run(port=8080, host='127.0.0.1', debug=True)
