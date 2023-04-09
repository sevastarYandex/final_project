from flask_restful import abort, Resource
from . import db_session
from .word import Word
from .user import User
from flask import jsonify
from .parser import word_parser
fields = ('id', 'word', 'translation_list', 'user_id', 'is_public')


def abort_if_word_not_found(word_id):
    session = db_session.create_session()
    word = session.query(Word).get(word_id)
    if not word:
        abort(404, error=f'word with id={word_id} is not found')


class WordResource(Resource):
    def get(self, word_id):
        abort_if_word_not_found(word_id)
        db_sess = db_session.create_session()
        word = db_sess.query(Word).get(word_id)
        resp = word.to_dict(only=fields)
        user_nick = db_sess.query(User).get(resp['user_id']).to_dict(
            only=('nick',))['nick']
        resp['user_nick'] = user_nick
        del resp['user_id']
        return jsonify({'word': resp})

    def delete(self, word_id):
        abort_if_word_not_found(word_id)
        db_sess = db_session.create_session()
        word = db_sess.query(Word).get(word_id)
        db_sess.delete(word)
        db_sess.commit()
        return jsonify({'success': 'ok'})

    def put(self, word_id):
        abort_if_word_not_found(word_id)
        db_sess = db_session.create_session()
        word = db_sess.query(Word).get(word_id)
        args = word_parser.parse_args()
        if args['user_id'] != word.user_id:
            return jsonify({'error': 'impossible to change host'})
        if args['word'] != word.word:
            return jsonify({'error': 'impossible to change word root'})
        db_sess.delete(word)
        word = Word()
        word.word = args['word']
        word.translation_list = args['translation_list']
        word.user_id = args['user_id']
        word.is_public = args['is_public']
        db_sess.add(word)
        db_sess.commit()
        return jsonify({'success': 'ok'})


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users':
                            [user.to_dict(only=fields)
                             for user in users]})

    def post(self):
        args = user_parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == args['email']).all():
            return jsonify(
                {'error': f'email "{args["email"]}" is already used'}
            )
        user = User()
        user.email = args['email']
        user.nick = args['nick']
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'ok'})
