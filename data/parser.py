from flask_restful import reqparse


user_parser = reqparse.RequestParser()
user_parser.add_argument('id', required=True, type=int)
user_parser.add_argument('nick', required=True)
user_parser.add_argument('email', required=True)
