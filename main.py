from flask import Flask, render_template, request

from admin import admin_bp
from blueprints.schedule_api import schedule_get
from data import db_session
from forms.schedule_form import ScheduleForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(admin_bp, url_prefix='/admin')


@app.route('/')
def index():
    """Прогружает главную страницу"""
    return render_template('buttons_main.html')


def clear_table(form):
    for day in range(6):
        for lesson in range(7):
            form.days.entries[day].lessons.entries[lesson].subject.data = ''


@app.route('/schedule', methods=['GET', 'POST'])
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
            return render_template('schedule.html', form=form)
        else:
            clear_table(form)
            return render_template('schedule.html', message='Для этого класса расписания не найдено', form=form)

    return render_template('schedule.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
