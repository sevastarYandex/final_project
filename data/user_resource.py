from flask_restful import abort, Resource
from . import db_session
from .user import User
from flask import jsonify
from .parser import user_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'user with id={user_id} is not found')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=('id', 'nick', 'email'))})

    def delete(self, user_id):
        pass

    def put(self, user_id):
        pass


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users':
                            [user.to_dict(
                                only=('id', 'nick', 'email'))
                                for user in users]})

    def post(self):
        pass
