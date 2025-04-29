from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

import blueprints.canteen_api
import blueprints.schedule_api
import blueprints.teachers_api
from blueprints.schedule_api import schedule_get
from blueprints.user_api import create_user
from data import db_session
from data.models_all.users import User
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.schedule_form import ScheduleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
app.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
app.register_blueprint(blueprints.canteen_api.canteen_bp, url_prefix='/api')
app.register_blueprint(blueprints.teachers_api.teachers_bp, url_prefix='/api')
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
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, title='Войти', message='Неверный логин или пароль')
    return render_template('login.html', form=form, title='Войти', message='')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        user_data = {
            'surname': form.surname.data,
            'name': form.name.data,
            'second_name': form.second_name.data,
            'email': form.email.data,
            'speciality': form.speciality.data,
            'age': form.date_bd.data
        }
        response = create_user(user_data).json
        if response.status_code == 201:
            return redirect('/login')
        error_data = response.json()
        return render_template('register.html', form=form, title='Регистрация', message=error_data.get('error'),
                               edit=False)
    return render_template('register.html', form=form, title='Регистрация', message='', edit=False)


def clear_table(form):
    for day in range(6):
        for lesson in range(7):
            form.days.entries[day].lessons.entries[lesson].subject.data = ''


@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    form = ScheduleForm(is_editing=False)
    if request.method == 'POST':
        json = schedule_get(f'{request.form["grade_level"]}_{request.form["class_word"]}')
        if json:
            for elem in json.json['schedule']:
                day = int(elem['day_of_week'])
                lesson_index = elem['number_lesson']
                subject_name = elem['subject']['subject_name']

                form.days.entries[day].lessons.entries[lesson_index].subject.data = subject_name
            return render_template('schedule.html', form=form)
        else:
            clear_table(form)
            return render_template('schedule.html', message='Для этого класса расписания не найдено', form=form)
    return render_template('schedule.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=5000, host='127.0.0.1', debug=True)
