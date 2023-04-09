from flask import Flask, render_template, redirect
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_restful import Api
from data import db_session
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_name = 'db/eng_db.db'


def init_data():
    if os.path.exists(db_name):
        return
    db_session.global_init(db_name)


def main():
    try:
        init_data()
    except Exception:
        print('error: please close database in other apps')
        exit(0)
    api = Api(app)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
