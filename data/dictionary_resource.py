from flask_restful import abort, Resource
from . import db_session
from .user import User
from .word import Word
from .dictionary import Dictionary
from flask import jsonify
from .parser import dictionary_parser
# fields = ('id', 'title', 'description', 'word_id', 'user_id', 'is_public')
#
#
# def abort_if_dictionary_not_found(dictionary_id):
#     session = db_session.create_session()
#     dictionary = session.query(Word).get(dictionary_id)
#     if not dictionary:
#         abort(404, error=f'dictionary with id={dictionary_id} is not found')
#
#
# class DictionaryResource(Resource):
#     def get(self, dictionary_id):
#         abort_if_dictionary_not_found(dictionary_id)
#         db_sess = db_session.create_session()
#         dictionary = db_sess.query(Dictionary).get(dictionary_id)
#         resp = dictionary.to_dict(only=fields)
#         words = list(map(
#             lambda x: db_sess.query(Word).get(int(x)).to_dict(only=('word',))['word'],
#             dictionary.to_dict(only=('word_id',))['word_id'].split(', ')))
#         del resp['word_id']
#         resp['words'] = words
#         return jsonify({'dictionary': resp})
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
# class DictionaryListResource(Resource):
#     def get(self):
#         db_sess = db_session.create_session()
#         dictionaries = db_sess.query(Dictionary).all()
#         return jsonify({'dictionaries':
#                             [dictionary.to_dict(only=fields)
#                              for dictionary in dictionaries]})
#
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
