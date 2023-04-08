from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_restful import Api
from data import db_session
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_name = 'db/music_db.db'


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def init_data():
    if os.path.exists(db_name):
        os.remove(db_name)
    db_session.global_init(db_name)


def main():
    init_data()
    api = Api(app)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
