from flask_restful import abort, Resource
from . import db_session
from .user import User
from .word import Word
from .dict import Dict
from flask import jsonify
from .parser import word_post_parser, word_put_parser
from .constant import US_FIELDS, WD_FIELDS, DC_FIELDS


def abort_if_word_not_found(word_id):
    session = db_session.create_session()
    word = session.query(Word).get(word_id)
    if not word:
        abort(404, message=f'word with id={word_id} is not found')


class WordRes(Resource):
    def get(self, word_id):
        abort_if_word_not_found(word_id)
        session = db_session.create_session()
        word = session.query(Word).get(word_id)
        resp = word.to_dict(only=WD_FIELDS)
        user = session.query(User).get(resp['user_id'])
        del resp['user_id']
        user = user.to_dict(only=US_FIELDS)
        resp['user'] = user
        dicts = session.query(Dict).all()
        dicts = [dict.to_dict(only=DC_FIELDS) for dict in dicts
                 if word_id in list(map(int, dict.wd_ids.split(', ')))]
        for i in range(len(dicts)):
            dict = dicts[i]
            dict['wd_ids'] = list(map(int, dict['wd_ids'].split(', ')))
            dicts[i] = dict
        resp['dicts'] = dicts
        return jsonify({'message': 'ok', 'resp': {'word': resp}})

    def delete(self, word_id):
        abort_if_word_not_found(word_id)
        session = db_session.create_session()
        word = session.query(Word).get(word_id)
        session.delete(word)
        session.commit()
        return jsonify({'message': 'ok'})

    def put(self, word_id):
        abort_if_word_not_found(word_id)
        session = db_session.create_session()
        word = session.query(Word).get(word_id)
        args = word_put_parser.parse_args()
        if args['word'] != word.word and \
                session.query(Word).filter(Word.word == args['word'],
                                           Word.user_id == word.user_id).all():
            return jsonify({'message': f'user with id={word.user_id} already has '
                                       f'word "{args["word"]}"'})
        id = word.id
        user_id = word.user_id
        session.delete(word)
        word = Word()
        word.id = id
        word.user_id = user_id
        word.word = args['word']
        word.tr_list = args['tr_list']
        word.is_pb = args['is_pb']
        session.add(word)
        session.commit()
        return jsonify({'message': 'ok'})


class WordListRes(Resource):
    def get(self):
        session = db_session.create_session()
        words = session.query(Word).all()
        return jsonify(
            {
                'message': 'ok',
                'resp': {
                    'words': [
                        word.to_dict(only=WD_FIELDS) for word in words
                    ]
                }
            }
        )

    def post(self):
        args = word_post_parser.parse_args()
        session = db_session.create_session()
        if session.query(Word).filter(Word.word == args['word']).all():
            return jsonify({'message': f'word "{args["word"]}" already exists'})
        word = Word()
        word.word = args['word']
        word.tr_list = args['tr_list']
        word.user_id = args['user_id']
        word.is_pb = args['is_pb']
        session.add(word)
        session.commit()
        return jsonify({'message': 'ok'})
