from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_restful import Api
from sqlalchemy.util.typing import ArgsTypeProcotol
import blueprints.schedule_api
from data import db_session
from data.models_all.schedule import Schedule
from data.models_all.users import User
from forms.schedule_form import ScheduleForm
from blueprints.schedule_api import schedule_get
from blueprints.user_api import create_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
app.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
@app.route('/index')
def index():
    """Прогружает главную страницу"""

    return render_template('base.html')


@app.route('/login')
def login():
    pass


@app.route('/register')
def register():
    pass


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    form = ScheduleForm(is_editing=False)
    if request.method == 'POST':
        json = schedule_get(f'{request.form["grade_level"]}_{request.form["class_word"]}').json
    return render_template('schedule.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
