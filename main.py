import sqlalchemy.orm
from flask import Flask, render_template, redirect, make_response, jsonify
from flask_login import LoginManager
from flask_restful import Api
from data import db_session
from data import constant
from data.user import User
from data.word import Word
from data.dict import Dict
from data.user_res import UserRes, UserListRes
from data.word_res import WordRes, WordListRes
from data.dict_res import DictRes, DictListRes


app = Flask(__name__)
app.config['SECRET_KEY'] = constant.SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
db_name = constant.DB_NAME


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'message': 'not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'message': 'bad request'}), 400)


def init_data():
    try:
        db_session.global_init(db_name)
    except Exception:
        print('message: database is opened in ohter apps')
        exit(0)
    # session = db_session.create_session()
    # user = User()
    # user.id = 1
    # user.nick = 'admin228'
    # user.email = 'admin228@gmail.com'
    # user.set_psw('__admin228__')
    # session.add(user)
    # word = Word()
    # word.id = 1
    # word.word = 'word'
    # word.tr_list = 'слово'
    # word.user_id = 1
    # word.is_pb = True
    # session.add(word)
    # dict = Dict()
    # dict.id = 1
    # dict.title = 'my dictionary'
    # dict.desc = 'cool dictionary'
    # dict.wd_ids = '1'
    # dict.user_id = 1
    # dict.is_pb = True
    # session.add(dict)
    # session.commit()


def main():
    init_data()
    api = Api(app)
    api.add_resource(UserRes, '/api/user/<int:user_id>')
    api.add_resource(UserListRes, '/api/user')
    api.add_resource(WordRes, '/api/word/<int:word_id>')
    api.add_resource(WordListRes, '/api/word')
    api.add_resource(DictRes, '/api/dict/<int:dict_id>')
    api.add_resource(DictListRes, '/api/dict')
    app.run(port=constant.PORT, host=constant.HOST)


if __name__ == '__main__':
    # main()
    help(sqlalchemy.orm.relationship)
