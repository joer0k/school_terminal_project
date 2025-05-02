from flask import Flask, render_template, request

from admin import admin_bp
from blueprints.schedule_api import schedule_get, classes_get
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
    classes = []
    if request.method == 'POST':
        json = schedule_get()
        if json is not None:
            result = {}
            for item in json.json['schedule']:
                class_name = f'{item["class_name"]["grade_level"]}_{item["class_name"]["class_word"]}'
                if class_name not in result.keys():
                    result[class_name] = [{
                        'classroom_id': item['classroom_id'],
                        'day_of_week': item['day_of_week'],
                        'number_lesson': item['number_lesson'],
                        'subject': item['subject']['subject_name']
                    }]
                else:
                    result[class_name] += [{
                        'classroom_id': item['classroom_id'],
                        'day_of_week': item['day_of_week'],
                        'number_lesson': item['number_lesson'],
                        'subject': item['subject']['subject_name']
                    }]
            classes = classes_get().json
            # for elem in json.json['schedule']:
            #     day = int(elem['day_of_week'])
            #     lesson_index = elem['number_lesson']
            #     subject_name = elem['subject']['subject_name']
            #
            #     form.days.entries[day].lessons.entries[lesson_index].subject.data = subject_name
            print(result)
            return render_template('schedule.html', form=form, data=result, classes=classes)
        else:
            clear_table(form)
            return render_template('schedule.html', form=form, message='Для этого класса расписания не найдено',
                                   data=[])

    return render_template('schedule.html', form=form, classes=classes)


'''помоги решить задачу. у меня есть страница с таблицей расписания(6 столбцов и 7 строк. столбцы - дни недели, строки - номера уроков) есть выпадающий список - выбор класса (с 5 по 11) и'''

if __name__ == '__main__':
    db_session.global_init('db/information.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
