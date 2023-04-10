from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager
from flask_restful import Api
from data import db_session
from data.user import User
from data.word import Word
from data.dict import Dictionary
from data.user_resource import UserResource, UserListResource
from data.word_resource import WordResource, WordListResource
from data.dictionary_resource import DictionaryResource, DictionaryListResource
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_name = 'db/eng_db.db'


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
    db_sess = db_session.create_session()
    user = User()
    user.nick = 'admin228'
    user.email = 'admin228@gmail.com'
    user.set_password('__admin228__')
    word = Word()
    word.word = 'word'
    word.translation_list = 'слово'
    word.user_id = 1
    word.is_public = True
    dictionary = Dictionary()
    dictionary.title = 'my dictionary'
    dictionary.description = 'cool dictionary'
    dictionary.word_id = '1'
    dictionary.user_id = 1
    dictionary.is_public = True
    db_sess.add(user)
    db_sess.add(word)
    db_sess.add(dictionary)
    db_sess.commit()


def main():
    try:
        init_data()
    except Exception:
        print('error: please close database in other apps')
        exit(0)
    api = Api(app)
    api.add_resource(UserResource, '/api/user/<int:user_id>')
    api.add_resource(UserListResource, '/api/user')
    api.add_resource(WordResource, '/api/word/<int:word_id>')
    api.add_resource(WordListResource, '/api/word')
    api.add_resource(DictionaryResource, '/api/dictionary/<int:dictionary_id>')
    api.add_resource(DictionaryListResource, '/api/dictionary')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
