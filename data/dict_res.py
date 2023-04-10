from flask_restful import abort, Resource
from . import db_session
from .user import User
from .word import Word
from .dict import Dict
from flask import jsonify
from .parser import dict_put_parser, dict_post_parser
from constant import US_FIELDS, WD_FIELDS, DC_FIELDS


def abort_if_dict_not_found(dict_id):
    session = db_session.create_session()
    dict = session.query(Dict).get(dict_id)
    if not dict:
        abort(404, message=f'dict with id={dict_id} is not found')


class DictRes(Resource):
    def get(self, dict_id):
        abort_if_dict_not_found(dict_id)
        session = db_session.create_session()
        dict = session.query(Dict).get(dict_id)
        resp = dict.to_dict(only=DC_FIELDS)
        return jsonify({'message': 'ok', 'resp': {'dict': resp}})
#
#     def delete(self, dictionary_id):
#         abort_if_dictionary_not_found(dictionary_id)
#         db_sess = db_session.create_session()
#         dictionary = db_sess.query(Dictionary).get(dictionary_id)
#         db_sess.delete(dictionary)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#     def put(self, dictionary_id):
#         abort_if_dictionary_not_found(dictionary_id)
#         db_sess = db_session.create_session()
#         dictionary = db_sess.query(Dictionary).get(dictionary_id)
#         args = dictionary_parser.parse_args()
#         if args['user_id'] != dictionary.user_id:
#             return jsonify({'error': 'impossible to change host'})
#         if args['title'] != dictionary.title and \
#                 args['title'] in \
#                 list(map(
#                     lambda x: x.to_dict(only=('title',))['title'],
#                     db_sess.query(Dictionary).filter(
#                         Dictionary.title == args['title']).all())):
#             return jsonify({'error': ''})
#         id = dictionary.to_dict(only=('id',))['id']
#         db_sess.delete(dictionary)
#         dictionary = Dictionary()
#         dictionary.id = id
#         dictionary.title = args['title']
#         dictionary.description = args['description']
#         dictionary.word_id = args['word_id']
#         dictionary.user_id = args['user_id']
#         dictionary.is_public = args['is_public']
#         db_sess.add(dictionary)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#
class DictListRes(Resource):
    def get(self):
        session = db_session.create_session()
        dicts = session.query(Dict).all()
        return jsonify(
            {
                'dicts': [
                    dict.to_dict(only=DC_FIELDS) for dict in dicts
                ]
            }
        )

#     def post(self):
#         args = dictionary_parser.parse_args()
#         db_sess = db_session.create_session()
#         if not db_sess.query(Dictionary).get(args['user_id']):
#             return jsonify({'error': f'user with id={args["user_id"]} is not found'})
#         #
#         dictionary = Dictionary()
#         dictionary.title = args['title']
#         dictionary.description = args['description']
#         dictionary.word_id = args['word_id']
#         dictionary.user_id = args['user_id']
#         dictionary.is_public = args['is_public']
#         db_sess.add(dictionary)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
