from flask import Flask
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

if __name__ == '__main__':
    db_session.global_init('db/school_canteen.db')
