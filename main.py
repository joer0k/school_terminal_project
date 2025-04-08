from flask import Flask
from data import db_canteen, db_schedule

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

if __name__ == '__main__':
    db_canteen.global_init('db/canteen.db')
    db_schedule.global_init('db/schedule.db')

    # app.run(port=8080, host='127.0.0.1', debug=True)
