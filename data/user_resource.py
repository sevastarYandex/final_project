from flask_restful import abort, Resource
from . import db_session
from .user import User
from flask import jsonify
from .parser import user_parser
# fields = ('id', 'nick', 'email', 'hashed_password')
#
#
# def abort_if_user_not_found(user_id):
#     session = db_session.create_session()
#     user = session.query(User).get(user_id)
#     if not user:
#         abort(404, error=f'user with id={user_id} is not found')
#
#
# class UserResource(Resource):
#     def get(self, user_id):
#         abort_if_user_not_found(user_id)
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).get(user_id)
#         resp = user.to_dict(only=fields)
#         words = list(map(
#             lambda x: x.to_dict(only=('word',))['word'], user.words
#         ))
#         dictionaries = list(map(
#             lambda x: x.to_dict(only=('title',))['title'], user.dictionaries
#         ))
#         resp['words'] = words
#         resp['dictionaries'] = dictionaries
#         return jsonify({'user': resp})
#
#     def delete(self, user_id):
#         abort_if_user_not_found(user_id)
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).get(user_id)
#         db_sess.delete(user)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#     def put(self, user_id):
#         abort_if_user_not_found(user_id)
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).get(user_id)
#         args = user_parser.parse_args()
#         if db_sess.query(User).filter(User.email == args['email']).all():
#             return jsonify(
#                 {'error': f'email "{args["email"]}" is already used'}
#             )
#         id = user.to_dict(only=('id',))['id']
#         db_sess.delete(user)
#         user = User()
#         user.id = id
#         user.nick = args['nick']
#         user.email = args['email']
#         user.set_password(args['password'])
#         db_sess.add(user)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
#
#
# class UserListResource(Resource):
#     def get(self):
#         db_sess = db_session.create_session()
#         users = db_sess.query(User).all()
#         return jsonify({'users':
#                             [user.to_dict(only=fields)
#                              for user in users]})
#
#     def post(self):
#         args = user_parser.parse_args()
#         db_sess = db_session.create_session()
#         if db_sess.query(User).filter(User.email == args['email']).all():
#             return jsonify(
#                 {'error': f'email "{args["email"]}" is already used'}
#             )
#         user = User()
#         user.email = args['email']
#         user.nick = args['nick']
#         user.set_password(args['password'])
#         db_sess.add(user)
#         db_sess.commit()
#         return jsonify({'success': 'ok'})
