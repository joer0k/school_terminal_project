from flask import Flask, render_template

from api.teachers_api import teachers_blueprint
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.register_blueprint(teachers_blueprint, url_prefix='/api')

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    db_session.global_init('db/schedule.db')
    app.run(port=5000, host='127.0.0.1', debug=True)
