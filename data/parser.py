from flask_restful import reqparse


user_parser = reqparse.RequestParser()
user_parser.add_argument('nick', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)

word_parser = reqparse.RequestParser()
word_parser.add_argument('word', required=True)
word_parser.add_argument('translation_list', required=True)
word_parser.add_argument('user_id', required=True, type=int)
word_parser.add_argument('is_public', required=True, type=bool)
