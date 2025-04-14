from flask import Flask, render_template, request
from flask_restful import Api
# from sqlalchemy.util.typing import ArgsTypeProcotol
import blueprints.schedule_bp
from data import db_session
from data.models_all.schedule import Schedule
from api.teachers_api import teachers_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.register_blueprint(blueprints.schedule_bp.blueprint)
app.register_blueprint(teachers_blueprint, url_prefix='/api')


@app.route('/')
@app.route('/index')
def index():
    """Прогружает главную страницу"""
    return render_template('base.html')


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=5000, host='127.0.0.1', debug=True)
