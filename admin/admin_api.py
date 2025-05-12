import os

import requests
from flask import render_template, request, redirect, current_app, url_for
from flask_login import login_user, login_required, logout_user, current_user

import blueprints.canteen_api
import blueprints.schedule_api
import blueprints.teachers_api
import blueprints.post_api
from admin import admin_bp
from admin.forms.add_dish_form import AddDishForm
from admin.forms.add_teacher_form import AddTeacherForm
from admin.forms.login_form import LoginForm
from admin.forms.menu_edit_form import MenuEditForm
from admin.forms.register_form import RegisterForm
from blueprints.post_api import get_posts
from blueprints.schedule_api import schedule_get, parallel_get
from blueprints.teachers_api import get_teachers
from blueprints.user_api import create_user

from data import db_session
from data.models_all.categories import Categories
from data.models_all.dishes import dish_to_weekday, Dishes
from data.models_all.teachers import Posts, Teachers
from data.models_all.users import User
from data.models_all.weekday import Weekday
from forms.schedule_form import ScheduleForm

admin_bp.register_blueprint(blueprints.schedule_api.schedule_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.user_api.users_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.canteen_api.canteen_bp, url_prefix='/api')
admin_bp.register_blueprint(blueprints.teachers_api.teachers_blueprint, url_prefix='/api')
admin_bp.register_blueprint(blueprints.post_api.posts_blueprint, url_prefix='/api')


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
            classes = [f'{form.grade_level.data}_{elem}' for elem in
                       parallel_get(int(form.grade_level.data)).json[form.grade_level.data]]
            return render_template('admin/schedule.html', form=form, data=result, classes=classes,
                                   title='Расписание занятий')
    else:
        return render_template('admin/schedule.html', form=form,
                               data=[], title='Расписание занятий')
    return render_template('admin/schedule.html', form=form, title='Расписание занятий')


@login_required
@admin_bp.route('/dishes')
def admin_dishes():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    dishes = requests.get('http://127.0.0.1:8080/api/dishes').json()['dishes']
    session = db_session.create_session()
    categories = [category.dish_category for category in session.query(Categories).all()]
    return render_template('admin/dishes.html', dishes=dishes, categories=categories)


@login_required
@admin_bp.route('/add_dish', methods=["GET", "POST"])
def add_dish():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    dish_form = AddDishForm()
    if dish_form.validate_on_submit():
        image_file = dish_form.image.data
        if image_file:
            filename = image_file.filename
            image_path = os.path.join('data/static/images/dishes/', filename)
            image_file.save(image_path)
        else:
            image_path = os.path.join('data/static/images/', "default.jpg")
        session = db_session.create_session()
        category_id = session.query(Categories).filter_by(dish_category=dish_form.categories.data).first().id
        dish = Dishes(
            id_categories=category_id,
            dish_name=dish_form.dish_name.data,
            image=image_path,
            description=dish_form.description.data if dish_form.description.data else "Не указано"
        )
        session.add(dish)
        session.commit()
        return redirect("/admin/dishes")
    return render_template("admin/add_dish.html", form=dish_form)


@login_required
@admin_bp.route('/edit_dish/<int:dish_id>', methods=["GET", "POST"])
def edit_dish(dish_id):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    dish_form = AddDishForm()
    session = db_session.create_session()
    dish = session.query(Dishes).get(dish_id)
    if request.method == "GET":
        dish_form = AddDishForm(obj=dish)
        category = session.query(Categories).get(dish.id_categories)
        dish_form.categories.data = category.dish_category
    elif request.method == "POST":
        if dish_form.validate_on_submit():
            image_file = dish_form.image.data
            if image_file:
                filename = image_file.filename
                image_path = os.path.join('/static/images/dishes/', filename)
                image_file.save(image_path)
            elif not dish.image:
                image_path = os.path.join('/static/images/', "default.jpg")
            else:
                image_path = dish.image
            category_id = session.query(Categories).filter_by(dish_category=dish_form.categories.data).first().id
            dish.id_categories = category_id
            dish.dish_name = dish_form.dish_name.data
            dish.image = image_path
            dish.description = dish_form.description.data if dish_form.description.data else "Не указано"
            session.commit()
            return redirect(url_for("admin.admin_dishes"))
    return render_template("admin/edit_dish.html", form=dish_form, dish=dish)


@login_required
@admin_bp.route('/canteen_menu')
def canteen_menu():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    with db_session.create_session() as session:
        weekdays = session.query(Weekday).order_by(Weekday.id).all()
        return render_template('admin/canteen_menu.html', weekdays=weekdays)


@login_required
@admin_bp.route('/menu_edit/<int:weekday_id>', methods=["GET", "POST"])
def menu_edit(weekday_id):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    menu_form = MenuEditForm()
    with db_session.create_session() as session:
        day = session.query(Weekday).get(weekday_id)
        if request.method == "GET":
            menu_form = MenuEditForm(is_editing=True, day=day)
            menu_form.weekday.data = day.weekday
        if request.method == "POST":
            if menu_form.validate_on_submit():
                selected = []
                for field in [
                    menu_form.first_dish_1, menu_form.first_dish_2, menu_form.first_dish_3, menu_form.first_dish_4,
                    menu_form.second_dish_1, menu_form.second_dish_2, menu_form.second_dish_3, menu_form.second_dish_4,
                    menu_form.drinks_1, menu_form.drinks_2, menu_form.drinks_3, menu_form.drinks_4
                ]:
                    if field.data != '-- Отсутствует --':
                        selected.append(field.data)
                session.execute(dish_to_weekday.delete().where(dish_to_weekday.c.weekday == weekday_id))
                dishes_id = [dish.id for dish in session.query(Dishes).filter(Dishes.dish_name.in_(selected))]
                for dish_id in dishes_id:
                    session.execute(
                        dish_to_weekday.insert().values(dishes=dish_id, weekday=weekday_id)
                    )
                    session.commit()
                return redirect("/admin/dishes")
    return render_template("admin/menu_edit.html", form=menu_form)


@admin_bp.route('/add_teacher', methods=["GET", "POST"])
def add_teacher():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
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
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    teachers = get_teachers().json['teachers']
    posts = get_posts().json['posts']
    return render_template('admin/teachers.html', teachers=teachers, posts=posts)


@admin_bp.route('/edit_teacher/<int:teacher_id>', methods=["GET", "POST"])
def admin_edit_teachers(teacher_id):
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
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
