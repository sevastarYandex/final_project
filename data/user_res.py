from flask_restful import abort, Resource
from flask import jsonify
from . import db_session
from .user import User
from .word import Word
from .dict import Dict
from .parser import user_parser
from .constant import US_FIELDS, WD_FIELDS, DC_FIELDS


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
        resp = user.to_dict(only=US_FIELDS)
        user_words = list(map(
            lambda x: x.to_dict(only=WD_FIELDS),
            session.query(Word).filter(
            Word.user_id == user_id).all()))
        other_words = list(map(
            lambda x: x.to_dict(only=WD_FIELDS),
            session.query(Word).filter(
            Word.user_id != user_id, Word.is_pb == True).all()))
        user_dicts = list(map(
            lambda x: x.to_dict(only=DC_FIELDS),
            session.query(Dict).filter(
            Dict.user_id == user_id).all()
        ))
        other_dicts = list(map(
            lambda x: x.to_dict(only=DC_FIELDS),
            session.query(Dict).filter(
            Dict.user_id != user_id, Dict.is_pb == True).all()
        ))
        for i in range(len(user_dicts)):
            dict = user_dicts[i]
            if not dict['wd_ids']:
                dict['wd_ids'] = []
            else:
                dict['wd_ids'] = list(map(int, dict['wd_ids'].split(', ')))
            user_dicts[i] = dict
        for i in range(len(other_dicts)):
            dict = other_dicts[i]
            if not dict['wd_ids']:
                dict['wd_ids'] = []
            else:
                dict['wd_ids'] = list(map(int, dict['wd_ids'].split(', ')))
            other_dicts[i] = dict
        resp['user_words'] = user_words
        resp['other_words'] = other_words
        resp['user_dicts'] = user_dicts
        resp['other_dicts'] = other_dicts
        return jsonify({'message': 'ok', 'resp': {'user': resp}})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        for word in session.query(Word).filter(Word.user_id == user_id).all():
            session.delete(word)
            for dict in session.query(Dict).all():
                if not dict.wd_ids:
                    continue
                wd_ids = list(map(int, dict.wd_ids.split(', ')))
                if word.id in wd_ids:
                    wd_ids.remove(word.id)
                dict.wd_ids = ', '.join(map(str, wd_ids))
        for dict in session.query(Dict).filter(Dict.user_id == user_id).all():
            session.delete(dict)
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
        user.nick = args['nick']
        user.email = args['email']
        user.set_psw(args['psw'])
        session.commit()
        return jsonify({'message': 'ok'})


class UserListRes(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'message': 'ok',
                'resp': {
                    'users': [
                        user.to_dict(only=US_FIELDS) for user in users
                    ]
                }
            }
        )

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).all():
            return jsonify({
                'message': f'user with email="{args["email"]}" already exists'
            })
        user = User()
        user.email = args['email']
        user.nick = args['nick']
        user.set_psw(args['psw'])
        session.add(user)
        session.commit()
        return jsonify({'message': 'ok'})
