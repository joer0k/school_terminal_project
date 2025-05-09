from flask import render_template, request, redirect, current_app
from flask_login import login_user, login_required, logout_user, current_user

import blueprints.canteen_api
import blueprints.schedule_api
import blueprints.teachers_api
from admin import admin_bp
from admin.forms.login_form import LoginForm
from admin.forms.register_form import RegisterForm
from blueprints.schedule_api import schedule_get
from blueprints.user_api import create_user
from data import db_session
from data.models_all.users import User
from forms.schedule_form import ScheduleForm

admin_bp.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.canteen_api.canteen_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.teachers_api.teachers_bp, url_prefix='/api')


@login_required
@admin_bp.route('/')
def index():
    """Прогружает главную страницу"""
    return render_template('admin/main.html', title='Авторизация')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    '''Страница входа в аккаунт'''
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
    return redirect('/admin')


@admin_bp.route('/register')
def register():
    '''Страница регистрации'''
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


@admin_bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    '''Страница с расписанием, где можно изменить и добавить новое'''
    if not current_user.is_authenticated:  # проверяет, что пользователь зарегистрирован
        return current_app.login_manager.unauthorized()
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
            classes = sorted(result.keys())
            return render_template('admin/schedule.html', form=form, data=result, classes=classes,
                                   title='Расписание занятий')
    else:
        return render_template('admin/schedule.html', form=form,
                               data=[], title='Расписание занятий')
    return render_template('admin/schedule.html', form=form, title='Расписание занятий')
