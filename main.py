from flask import Flask, render_template, request
from flask_login import LoginManager

from admin import admin_bp
from blueprints.schedule_api import schedule_get, parallel_get
from data import db_session
from data.models_all.users import User
from forms.schedule_form import ScheduleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(admin_bp, url_prefix='/admin')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'


@login_manager.user_loader
def load_user(user_id):
    '''Инициализирует пользователя'''
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/')
def index():
    """Прогружает главную страницу"""
    return render_template('buttons_main.html')


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    '''Прогружает страницу с расписанием
    Метод POST заполняет таблицу с расписанием'''
    form = ScheduleForm()
    if request.method == 'POST':
        json = schedule_get(int(form.grade_level.data))
        if json is not None:
            result = {}
            for item in json.json['schedule']:
                class_name = f'{item["class_name"]["grade_level"]}_{item["class_name"]["class_word"]}'
                if class_name not in result.keys():
                    result[class_name] = {}
                day = item['weekday']['weekday']
                number = item['number_lesson']
                subject = item['subject']['subject_name']
                if day not in result[class_name].keys():
                    result[class_name][day] = {}
                result[class_name][day][number] = f'{subject} (каб. {item["classroom"]["room_number"]})'
            classes = [f'{form.grade_level.data}_{elem}' for elem in
                       parallel_get(int(form.grade_level.data)).json[form.grade_level.data]]
            return render_template('schedule.html', form=form, data=result, classes=classes, title='Расписание занятий')
    else:
        return render_template('schedule.html', form=form,
                               data=[], title='Расписание занятий')
    return render_template('schedule.html', form=form, title='Расписание занятий')


@app.route('/it_cube')
def it_cube():
    return render_template('it_cube.html', title='Центр цифрового образования детей «IT-куб»')


@app.route('/about_itcube')
def about_itcube():
    return render_template('about_itcube.html')


@app.route('/teachers')
def show_teachers():
    return render_template('team.html', title='Наш коллектив')


@app.route('/administration')
def show_administration():
    return render_template('administration.html', title='Администрация')


@app.route('/programs')
def programs_itcube():
    return render_template('programs_itcube.html', title='Направления')



if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
