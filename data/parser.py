from flask_restful import reqparse


user_parser = reqparse.RequestParser()
user_parser.add_argument('nick', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('psw', required=True)

word_put_parser = reqparse.RequestParser()
word_put_parser.add_argument('word', required=True)
word_put_parser.add_argument('tr_list', required=True)
word_put_parser.add_argument('is_pb', required=True, type=bool)

word_post_parser = word_put_parser
word_post_parser.add_argument('user_id', required=True, type=int)

dict_parser = reqparse.RequestParser()
dict_parser.add_argument('title', required=True)
dict_parser.add_argument('desc', required=True)
dict_parser.add_argument('wd_ids', required=True)
dict_parser.add_argument('is_pb', required=True, type=bool)
