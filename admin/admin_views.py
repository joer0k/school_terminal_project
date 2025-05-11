import os

import requests
from flask import render_template, request, redirect, url_for, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import blueprints.canteen_api
import blueprints.schedule_api
import blueprints.teachers_api
from admin import admin_bp
from admin.forms.add_teacher_form import AddTeacherForm
from blueprints.schedule_api import schedule_get
from blueprints.user_api import create_user
from data import db_session
from data.models_all.categories import Categories
from data.models_all.teachers import Posts, Teachers
from data.models_all.users import User
from data.models_all.weekday import Weekday
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.schedule_form import ScheduleForm

admin_bp.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.canteen_api.canteen_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.teachers_api.teachers_blueprint, url_prefix='/api')


@login_required
@admin_bp.route('/')
def index():
    """Прогружает главную страницу"""
    return render_template('admin/main.html', title='Авторизация')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('/admin')
        return render_template('admin/login.html', form=form, title='Войти', message='Неверный логин или пароль')
    return render_template('admin/login.html', form=form, title='Авторизация', message='')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/admin')


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

@admin_bp.route('/add_teacher', methods=["GET", "POST"])
def add_teacher():
    # if not current_user.is_authenticated:
    #     return current_app.login_manager.unauthorized()
    teacher_form = AddTeacherForm()
    if teacher_form.validate_on_submit():
        image_file = teacher_form.photo.data
        if image_file:
            filename = image_file.filename
            image_path = os.path.join('static/images/teachers/', filename)
            image_file.save(image_path)
        else:
            image_path = os.path.join('static/images/', "no_photo.jpg")
        session = db_session.create_session()
        post_id = session.query(Posts).filter_by(title=teacher_form.post.data).first().id
        teacher = Teachers(
            post_id=post_id,
            teacher_name=teacher_form.teacher_name.data,
            way_to_photo=image_path,
            additional_information=teacher_form.additional_information.data if teacher_form.additional_information.data else "Не указано"
        )
        session.add(teacher)
        session.commit()
        return redirect("/admin/teachers")
    return render_template("admin/add_teacher.html", form=teacher_form)


@admin_bp.route('/teachers')
def admin_teachers():
    # if not current_user.is_authenticated:
    #     return current_app.login_manager.unauthorized()
    teachers = requests.get('http://127.0.0.1:5000/api/teachers').json()['teachers']
    posts = requests.get('http://127.0.0.1:5000/api/posts').json()['posts']
    return render_template('admin/teachers.html', teachers=teachers, posts=posts)


@admin_bp.route('/edit_teacher/<int:teacher_id>', methods=["GET", "POST"])
def admin_edit_teachers(teacher_id):
    # if not current_user.is_authenticated:
    #     return current_app.login_manager.unauthorized()
    teacher_form = AddTeacherForm()
    session = db_session.create_session()
    teacher = session.query(Teachers).get(teacher_id)
    if request.method == "GET":
        teacher_form = AddTeacherForm(obj=teacher)
        post = session.query(Posts).get(teacher.post_id)
        teacher_form.post.data = post.title
    elif request.method == "POST":
        if teacher_form.validate_on_submit():
            image_file = teacher_form.photo.data
            if image_file:
                filename = image_file.filename
                image_path = os.path.join('static/images/teachers/', filename)
                image_file.save(image_path)
            elif not teacher.way_to_photo:
                image_path = os.path.join('static/images/', "default.jpg")
            else:
                image_path = teacher.way_to_photo
            post_id = session.query(Posts).filter_by(title=teacher_form.post.data).first().id
            teacher.post_id = post_id
            teacher.teacher_name = teacher_form.teacher_name.data
            teacher.way_to_photo = image_path
            teacher.additional_information = teacher_form.additional_information.data if teacher_form.additional_information.data else "Не указано"
            session.commit()
            return redirect(url_for("admin.admin_teachers"))
    return render_template("/admin/edit_teacher.html", form=teacher_form, teacher=teacher)

