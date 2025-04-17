from flask import Flask, render_template, request
from flask_restful import Api
from sqlalchemy.util.typing import ArgsTypeProcotol
import blueprints.schedule_bp
from data import db_session
from data.models_all.schedule import Schedule
from forms.schedule_form import ScheduleForm
from blueprints.schedule_bp import schedule_get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.register_blueprint(blueprints.schedule_bp.blueprint)


@app.route('/')
@app.route('/index')
def index():
    """Прогружает главную страницу"""
    return render_template('base.html')


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    form = ScheduleForm(is_editing=False)
    if request.method == 'POST':
        json = schedule_get(f'{request.form["grade_level"]}_{request.form["class_word"]}').json

    return render_template('schedule.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
