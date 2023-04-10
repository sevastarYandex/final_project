from flask_restful import abort, Resource
from . import db_session
from .user import User
from .word import Word
from .dict import Dict
from flask import jsonify
from .parser import word_parser
from .constant import WD_FIELDS


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
        resp = word.to_dict(only=fields)
        user = session.query(User).get(resp['user_id'])
        del resp['user_id']
        user = user.to_dict()
        return jsonify({'message': 'ok', 'resp': {'word': resp}})
#
#     def delete(self, word_id):
#         abort_if_word_not_found(word_id)
#         db_sess = db_session.create_session()
#         word = db_sess.query(Word).get(word_id)
#         db_sess.delete(word)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#     def put(self, word_id):
#         abort_if_word_not_found(word_id)
#         db_sess = db_session.create_session()
#         word = db_sess.query(Word).get(word_id)
#         args = word_parser.parse_args()
#         if args['user_id'] != word.user_id:
#             return jsonify({'error': 'impossible to change host'})
#         if args['word'] != word.word:
#             return jsonify({'error': 'impossible to change word root'})
#         id = word.to_dict(only=('id',))['id']
#         db_sess.delete(word)
#         word = Word()
#         word.id = id
#         word.word = args['word']
#         word.translation_list = args['translation_list']
#         word.user_id = args['user_id']
#         word.is_public = args['is_public']
#         db_sess.add(word)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#
class WordListRes(Resource):
    def get(self):
        session = db_session.create_session()
        words = session.query(Word).all()
        return jsonify(
            {
                'message': 'ok',
                'resp': {
                    'words': [
                        word.to_dict(only=fields) for word in words
                    ]
                }
            }
        )
#
#     def post(self):
#         args = word_parser.parse_args()
#         db_sess = db_session.create_session()
#         if not db_sess.query(User).get(args['user_id']):
#             return jsonify({'error': f'user with id={args["user_id"]} is not found'})
#         if args['word'] in list(map(lambda x: x.to_dict(only=('word',))['word'],
#                                     db_sess.query(Word).filter(
#                                         Word.user_id == args['user_id']).all())):
#             return jsonify({'error': f'user with id={args["user_id"]} '
#                                      f'already owns the word "{args["word"]}"'})
#         word = Word()
#         word.word = args['word']
#         word.translation_list = args['translation_list']
#         word.user_id = args['user_id']
#         word.is_public = args['is_public']
#         db_sess.add(word)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
