from flask import Flask, render_template, request
from flask_login import LoginManager

from admin import admin_bp
from blueprints.canteen_api import canteen_bp, get_week_menu
from blueprints.post_api import get_posts, get_one_post
from blueprints.schedule_api import schedule_get, parallel_get
from blueprints.teachers_api import get_teachers, get_one_teacher
from data import db_session
from data.models_all.users import User
from forms.schedule_form import ScheduleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(canteen_bp, url_prefix='/api')

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


@app.route('/team')
def teachers_page():
    return render_template('team.html')


@app.route('/page/<name>')
def administration(name):
    teachers = get_teachers().json['teachers']
    posts = get_posts().json['posts']
    title_dict = {'administration': 'Администрация гимназии 87', 'middle_school': 'Учителя средней школы гимназии 87',
                  'primary_school': 'Учителя начальной школы гимназии 87'}
    list_right_teachers = []
    for i in teachers:
        if posts[i['post_id'] - 1]['post'] == name:
            list_right_teachers.append(i)
    return render_template('page_with_teachers.html', json=list_right_teachers, posts=posts, title=title_dict[name])


@app.route('/page/more_detailed/<int:teacher_id>')
def more_detailed(teacher_id):
    teacher = get_one_teacher(teacher_id).json['teacher'][0]
    posts = get_one_post(int(teacher['post_id'])).json
    return render_template('more_detailed.html', json=teacher, posts=posts)


@app.route('/administration')
def show_administration():
    return render_template('administration.html', title='Администрация')


@app.route('/programs')
def programs_itcube():
    return render_template('programs_itcube.html', title='Направления')


@app.route('/canteen')
def canteen_page():
    menu = get_week_menu().json
    menu_data = []
    for item in menu["menu"]:
        menu_data.extend(item['dishes'])
    return render_template('canteen.html', title="Меню школьной столовой", menu=menu_data)


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
