"""py-file with dictionary resources"""


from flask_restful import abort, Resource
from . import db_session
from .user import User
from .word import Word
from .dict import Dict
from flask import jsonify
from .parser import dict_put_parser, dict_post_parser
from .constant import US_FIELDS, WD_FIELDS, DC_FIELDS


def abort_if_dict_not_found(dict_id):
    """function, raises abort-404 if dictionary with id=dict_id is not found"""
    session = db_session.create_session()
    dict = session.query(Dict).get(dict_id)
    if not dict:
        abort(404, message=f'dict with id={dict_id} is not found')


class DictRes(Resource):
    """class of the dict resource for operations on a dict with id=dict_id"""
    def get(self, dict_id):
        """format is
        {
          "message": message,
          "resp": {
            "dict": {
              "desc": description,
              "id": id,
              "is_pb": is_public,
              "title": title,
              "user": {
                "email": email,
                "hashed_psw": hashed_password,
                "id": user_id,
                "nick": nickname
              },
              "words": [
                {
                  "id": word_id,
                  "is_pb": is_public,
                  "tr_list": translation,
                  "user_id": host_id,
                  "word": word
                }, ...
              ]
            }
          }
        }"""
        abort_if_dict_not_found(dict_id)
        session = db_session.create_session()
        dict = session.query(Dict).get(dict_id)
        resp = dict.to_dict(only=DC_FIELDS)
        del resp['user_id']
        resp['user'] = dict.user.to_dict(only=US_FIELDS)
        if not dict.wd_ids:
            wd_ids = []
        else:
            wd_ids = list(map(int, dict.wd_ids.split(', ')))
        del resp['wd_ids']
        resp['words'] = []
        for wd_id in wd_ids:
            word = session.query(Word).get(wd_id).to_dict(only=WD_FIELDS)
            resp['words'].append(word)
        return jsonify({'message': 'ok', 'resp': {'dict': resp}})

    def delete(self, dict_id):
        abort_if_dict_not_found(dict_id)
        session = db_session.create_session()
        dict = session.query(Dict).get(dict_id)
        session.delete(dict)
        session.commit()
        return jsonify({'message': 'ok'})

    def put(self, dict_id):
        # host can't have two dicts with the same titles
        abort_if_dict_not_found(dict_id)
        session = db_session.create_session()
        dict = session.query(Dict).get(dict_id)
        args = dict_put_parser.parse_args()
        if args['title'] != dict.title and \
                session.query(Dict).filter(
                    Dict.user_id == dict.user_id,
                    Dict.title == args['title']).all():
            return jsonify({
                'message': f'user with id={dict.user_id} '
                           f'already has dict "{args["title"]}"'})
        if args['wd_ids']:
            for wd_id in args['wd_ids'].split(', '):
                try:
                    wd_id = int(wd_id)
                except Exception:
                    return jsonify({
                        'message': f'word with id="{wd_id}" is not found'
                    })
                if not session.query(Word).get(wd_id):
                    return jsonify({
                        'message': f'word with id={wd_id} is not found'
                    })
        dict.title = args['title']
        dict.desc = args['desc']
        dict.wd_ids = args['wd_ids']
        dict.is_pb = args['is_pb']
        session.commit()
        return jsonify({'message': 'ok'})


class DictListRes(Resource):
    """class of the dict resource for operations on a dict-table"""
    def get(self):
        """format is
        {
          "message": message,
          "resp": {
            "dicts": [
              {
                "desc": description,
                "id": dict_id,
                "is_pb": is_public,
                "title": title,
                "user_id": host_id,
                "wd_ids": [word_id, ...]
              }, ...
            ]
          }
        }"""
        session = db_session.create_session()
        dicts = []
        for dict in session.query(Dict).all():
            dict = dict.to_dict(only=DC_FIELDS)
            if not dict['wd_ids']:
                dict['wd_ids'] = []
            else:
                dict['wd_ids'] = list(map(int, dict['wd_ids'].split(', ')))
            dicts.append(dict)
        return jsonify({'message': 'ok',
                        'resp': {'dicts': dicts}})

    def post(self):
        # host can't have two dicts with the same titles
        args = dict_post_parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).get(args['user_id']):
            return jsonify({
                'message': f'user with id={args["user_id"]} is not found'
            })
        if session.query(Dict).filter(
                Dict.user_id == args['user_id'], Dict.title == args['title']
        ).all():
            return jsonify({
                'message': f'user with id={args["user_id"]} '
                           f'already has dict "{args["title"]}"'})
        if args['wd_ids']:
            for wd_id in args['wd_ids'].split(', '):
                try:
                    wd_id = int(wd_id)
                except Exception:
                    return jsonify({
                        'message': f'word with id="{wd_id}" is not found'
                    })
                if not session.query(Word).get(wd_id):
                    return jsonify({
                        'message': f'word with id={wd_id} is not found'
                    })
        dict = Dict()
        dict.title = args['title']
        dict.desc = args['desc']
        dict.wd_ids = args['wd_ids']
        dict.user_id = args['user_id']
        dict.is_pb = args['is_pb']
        session.add(dict)
        session.commit()
        return jsonify({'message': 'ok'})
