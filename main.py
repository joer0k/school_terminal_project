from flask import Flask, render_template, request
from sqlalchemy import values

import blueprints.schedule_bp
from data.schedule import db_schedule
from data.canteen import db_canteen

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
@app.route('/index')
def index():
    '''Прогружает главную страницу'''
    return render_template('main.html')


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        session = db_schedule.create_session()
    return render_template('schedule.html')


if __name__ == '__main__':
    db_canteen.global_init('db/canteen.db')
    db_schedule.global_init('db/schedule.db')
    app.register_blueprint(blueprints.schedule_bp.blueprint)
    app.run(port=8080, host='127.0.0.1', debug=True)
