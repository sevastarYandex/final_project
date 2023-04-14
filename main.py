import sqlalchemy.orm
from test import mpt
from requests import get, delete, post, put
from flask import Flask, render_template, redirect, make_response, jsonify, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api
from data import db_session
from data import constant
from data.user import User
from data.word import Word
from data.dict import Dict
from data.user_res import UserRes, UserListRes
from data.word_res import WordRes, WordListRes
from data.dict_res import DictRes, DictListRes
from forms.user import LoginForm, SigninForm, EditForm


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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/status/logout is successful')


def init_data():
    try:
        db_session.global_init(db_name)
    except Exception:
        print('message: database is opened in ohter apps')
        exit(0)
    session = db_session.create_session()
    if not session.query(User).get(1):
        user = User()
        user.id = 1
        user.nick = 'admin228'
        user.email = 'admin228@gmail.com'
        user.set_psw('__admin228__')
        session.add(user)
        word = Word()
        word.id = 1
        word.word = 'word'
        word.tr_list = 'слово'
        word.user_id = 1
        word.is_pb = True
        session.add(word)
        dict = Dict()
        dict.id = 1
        dict.title = 'my dictionary'
        dict.desc = 'cool dictionary'
        dict.wd_ids = '1'
        dict.user_id = 1
        dict.is_pb = True
        session.add(dict)
        session.commit()


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


@app.route('/status/<message>')
def status(message):
    return render_template('base.html', title='Action status', message=message)


@app.route('/')
@app.route('/welcome')
def welcome():
    session = db_session.create_session()
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = -1
    user_words = list(map(lambda x:
                          [f'{x.word} - {x.tr_list}', f'/word/{x.id}'],
                          session.query(Word).filter(Word.user_id == user_id).all()))
    user_dicts = list(map(lambda x:
                          [f'{x.title} - {x.desc}', f'/dict/{x.id}'],
                          session.query(Dict).filter(Dict.user_id == user_id).all()))
    pb_words = list(map(lambda x: [f'{x.word} '
                                   f'(owner - {session.query(User).get(x.user_id).nick})',
                                   f'/word/{x.id}'],
                        session.query(Word).filter(Word.is_pb, Word.user_id != user_id).all()))
    pb_dicts = list(map(lambda x: [f'{x.title} '
                                   f'(owner - {session.query(User).get(x.user_id).nick})',
                                   f'/dict/{x.id}'],
                        session.query(Dict).filter(Dict.is_pb, Dict.user_id != user_id).all()))
    if user_id == -1:
        data = [['Public words', pb_words],
                ['Public dictionaries', pb_dicts]]
    else:
        data = [['Your words', user_words],
                ['Public words', pb_words],
                ['Your dictionaries', user_dicts],
                ['Public dictionaries', pb_dicts]]
    return render_template('welcome.html', title=constant.TITLE, data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_psw(form.password.data):
            login_user(user)
            return redirect('/status/authorization is successful')
        return render_template('login.html',
                               message='wrong login or password',
                               form=form)
    return render_template('login.html', title='Log in', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signin.html', title=constant.TITLE,
                                   form=form,
                                   message="passwords are not equal")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('signin.html', title=constant.TITLE,
                                   form=form,
                                   message='email is already used')
        user = User()
        user.nick = form.nick.data
        user.email = form.email.data
        user.set_psw(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/status/registration is successful')
    return render_template('signin.html', title='Sign in', form=form)


@app.route('/user/<int:user_id>')
def user_page(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return redirect(f'/status/user with id={user_id} is not found')
    data = [user.id, user.nick, user.email]
    if current_user.is_authenticated:
        current_id = current_user.id
    else:
        current_id = -1
    if current_id == user_id:
        words = session.query(Word).filter(Word.user_id == user_id).all()
        words = list(map(lambda x: [f'{x.word} - {x.tr_list}', f'/word/{x.id}'], words))
        dicts = session.query(Dict).filter(Dict.user_id == user_id).all()
        dicts = list(map(lambda x: [f'{x.title} - {x.desc}', f'/dict/{x.id}'], dicts))
    else:
        words = session.query(Word).filter(Word.user_id == user_id, Word.is_pb).all()
        words = list(map(lambda x:
                         [x.word, f'/word/{x.id}'], words))
        dicts = session.query(Dict).filter(Dict.user_id == user_id, Dict.is_pb).all()
        dicts = list(map(lambda x:
                         [x.title, f'/dict/{x.id}'], dicts))
    return render_template('user_page.html',
                           title='User page', data=data, words=words, dicts=dicts)


@app.route('/word/<int:word_id>')
def word_page(word_id):
    session = db_session.create_session()
    word = session.query(Word).get(word_id)
    if not word:
        return redirect(f'/status/word with id={word_id} is not found')
    if current_user.is_authenticated:
        current_id = current_user.id
    else:
        current_id = -1
    if word.user_id != current_id and not word.is_pb:
        return redirect(f'/status/word with id={word_id} is private')
    user = session.query(User).get(word.user_id)
    data = [word.id, word.word, word.tr_list, word.is_pb, word.user_id]
    user_link = [user.nick, f'/user/{word.user_id}']
    dicts = session.query(Dict).filter((Dict.user_id == current_id) | Dict.is_pb).all()
    for dict in dicts:
        if word_id not in list(map(int, dict.wd_ids.split(', '))):
            dicts.remove(dict)
    dicts = list(map(lambda x:
                     [x.title + f' - {x.desc}' * (x.user_id == current_id) +
                      f' (owner - {session.query(User).get(x.user_id).nick})' *
                      (x.user_id != current_id), f'/dict/{x.id}'],
                     dicts))
    return render_template('word_page.html',
                           title='Word page', data=data, user=user_link, dicts=dicts)


@app.route('/dict/<int:dict_id>')
def dict_page(dict_id):
    session = db_session.create_session()
    dict = session.query(Dict).get(dict_id)
    if not dict:
        return redirect(f'/status/dict with id={dict_id} is not found')
    if current_user.is_authenticated:
        current_id = current_user.id
    else:
        current_id = -1
    if dict.user_id != current_id and not dict.is_pb:
        return redirect(f'/status/dict with id={dict_id} is private')
    user = session.query(User).get(dict.user_id)
    data = [dict.id, dict.title, dict.desc, dict.is_pb, dict.user_id]
    user_link = [user.nick, f'/user/{dict.user_id}']
    wd_ids = list(map(int, dict.wd_ids.split(', ')))
    words = session.query(Word).filter(Word.id.in_(wd_ids),
                                       (Word.user_id == current_id) | Word.is_pb).all()
    words = list(map(lambda x: [x.word + f' - {x.tr_list}' * (x.user_id == current_id) +
                                f' (owner - {session.query(User).get(x.user_id).nick})' *
                                (x.user_id != current_id), f'/word/{x.id}'],
                     words))
    return render_template('dict_page.html',
                           title='Dict page', data=data, user=user_link, words=words)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    session = db_session.create_session()
    form = EditForm()
    user = session.query(User).get(user_id)
    if not user:
        return redirect(f'/status/user with id={user_id} is not found')
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect('/status/access is denied')
        if current_user.id != user_id:
            return redirect('/status/access is denied')
        user = session.query(User).get(user_id)
        form.nick.data = user.nick
        form.email.data = user.email
    if form.validate_on_submit():
        answer = mpt(f'user/{user_id}', put,
                     {'nick': form.nick.data,
                      'email': form.email.data,
                      'psw': form.password.data})
        if answer['message'] == 'ok':
            return redirect('/status/changes are successful')
        return redirect(f'/status/{answer["message"]}')
    return render_template('edit_user.html', title='Edit user', form=form, user_id=user_id)

#
# @app.route('/delete_user/<int:user_id>', methods=['GET', 'DELETE'])
# @login_required
# def delete_user(user_id):
#     return ''
#
#
# @app.route('/post_word', methods=['GET', 'POST'])
# @login_required
# def post_word():
#     return ''
#
#
# @app.route('/edit_word/<int:word_id>', methods=['GET', 'PUT'])
# @login_required
# def edit_word(word_id):
#     return ''
#
#
# @app.route('/delete_word/<int:word_id>', methods=['GET', 'DELETE'])
# @login_required
# def delete_word(word_id):
#     return ''
#
#
# @app.route('/post_dict', methods=['GET', 'POST'])
# @login_required
# def post_dict():
#     return ''
#
#
# @app.route('/edit_dict/<int:dict_id>', methods=['GET', 'PUT'])
# @login_required
# def edit_dict(dict_id):
#     return ''
#
#
# @app.route('/delete_dict/<int:dict_id>', methods=['GET', 'DELETE'])
# @login_required
# def delete_dict(dict_id):
#     return ''


if __name__ == '__main__':
    main()
