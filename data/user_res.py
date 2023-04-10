from flask_restful import abort, Resource
from flask import jsonify
from . import db_session
from .user import User
from .parser import user_parser
fields = ('id', 'nick', 'email', 'hashed_psw')


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'user with id={user_id} is not found')


class UserRes(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        resp = user.to_dict(only=fields)
        words = list(map(
            lambda x: x.to_dict(only=('word',))['word'], user.words))
        dicts = list(map(
            lambda x: x.to_dict(only=('title',))['title'], user.dicts))
        resp['words'] = words
        resp['dicts'] = dicts
        return jsonify({'message': 'ok', 'resp': {'user': resp}})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'message': 'ok'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        args = user_parser.parse_args()
        if args['email'] != user.email and \
                session.query(User).filter(User.email == args['email']).all():
            return jsonify({'message':
                                f'user with email="{args["email"]}" already exists'})
        id = user.to_dict(only=('id',))['id']
        session.delete(user)
        user = User()
        user.id = id
        user.nick = args['nick']
        user.email = args['email']
        user.set_psw(args['psw'])
        session.add(user)
        session.commit()
        return jsonify({'message': 'ok'})


class UserListRes(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'message': 'ok',
                        'resp': {'users':
                                     [user.to_dict(only=fields)
                                      for user in users]}})

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).all():
            return jsonify({'message':
                                f'user with email="{args["email"]}" already exists'})
        user = User()
        user.email = args['email']
        user.nick = args['nick']
        user.set_psw(args['psw'])
        session.add(user)
        session.commit()
        return jsonify({'message': 'ok'})