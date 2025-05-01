from flask import render_template, request, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

import blueprints.canteen_api
import blueprints.schedule_api
import blueprints.teachers_api
from admin import admin_bp
from blueprints.schedule_api import schedule_get
from blueprints.user_api import create_user
from data import db_session
from data.models_all.users import User
from admin.forms.login_form import LoginForm
from admin.forms.register_form import RegisterForm
from forms.schedule_form import ScheduleForm

admin_bp.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.canteen_api.canteen_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.teachers_api.teachers_bp, url_prefix='/api')
# login_manager = LoginManager()
# login_manager.init_app(admin_bp)


# @login_manager.user_loader
# def load_user(user_id):
#     db_sess = db_session.create_session()
#     return db_sess.get(User, user_id)


@admin_bp.route('/')
def index():
    """Прогружает главную страницу"""
    return redirect('/admin/login')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('admin/login.html', form=form, title='Войти', message='Неверный логин или пароль')
    return render_template('admin/login.html', form=form, title='Войти', message='')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@admin_bp.route('/register')
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
        return render_template('/admin/register.html', form=form, title='Регистрация', message=error_data.get('error'),
                               edit=False)
    return render_template('/admin/register.html', form=form, title='Регистрация', message='', edit=False)


def clear_table(form):
    for day in range(6):
        for lesson in range(7):
            form.days.entries[day].lessons.entries[lesson].subject.data = ''


@admin_bp.route('/schedule', methods=['GET', 'POST', 'PUT'])
def schedule():
    form = ScheduleForm()
    if request.method == 'POST':
        json = schedule_get(f'{request.form["grade_level"]}_{request.form["class_word"]}')
        if json is not None:
            for elem in json.json['schedule']:
                day = int(elem['day_of_week'])
                lesson_index = elem['number_lesson']
                subject_name = elem['subject']['subject_name']

                form.days.entries[day].lessons.entries[lesson_index].subject.data = subject_name
            return render_template('/admin/schedule.html', form=form)
        else:
            clear_table(form)
            return render_template('/admin/schedule.html', message='Для этого класса расписания не найдено', form=form)
    if request.method == 'PUT':
        '''пока не работает, потому что в коде джаваскрипта нужно создавать список,
        где будут значения из таблицы, а это у меня не получилось'''
        print(request.data)
    return render_template('/admin/schedule.html', form=form)
