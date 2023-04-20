"""py-file with neccessary parsers (for post-/put-requests)"""


from flask_restful import reqparse


# user_parser - parser for getting info about user while making post-/put-requests
# arguments: nick (nickname), email, psw (password)
user_parser = reqparse.RequestParser()
user_parser.add_argument('nick', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('psw', required=True)

# word_put_parser - parser for getting info about word while making put-requests
# arguments: word (en-version), tr_list (ru-version), is_pb (is public)
word_put_parser = reqparse.RequestParser()
word_put_parser.add_argument('word', required=True)
word_put_parser.add_argument('tr_list', required=True)
word_put_parser.add_argument('is_pb', required=True, type=bool)

# word_post_parser - parser for getting info about word while making post-requests
# arguments: word (en-version), tr_list (ru-version), is_pb (is public), user_id (id of the host)
word_post_parser = reqparse.RequestParser()
word_post_parser.add_argument('word', required=True)
word_post_parser.add_argument('tr_list', required=True)
word_post_parser.add_argument('is_pb', required=True, type=bool)
word_post_parser.add_argument('user_id', required=True, type=int)

# dict_put_parser - parser for getting info about dict while making put-requests
# arguments: title, desc (description), wd_ids (ids of the words), is_pb (is public)
dict_put_parser = reqparse.RequestParser()
dict_put_parser.add_argument('title', required=True)
dict_put_parser.add_argument('desc', required=True)
dict_put_parser.add_argument('wd_ids', required=True)
dict_put_parser.add_argument('is_pb', required=True, type=bool)

# dict_post_parser - parser for getting info about dict while making post-requests
# arguments: title, desc (description), wd_ids (ids of the words), is_pb (is public), user_id (id of the host)
dict_post_parser = reqparse.RequestParser()
dict_post_parser.add_argument('title', required=True)
dict_post_parser.add_argument('desc', required=True)
dict_post_parser.add_argument('wd_ids', required=True)
dict_post_parser.add_argument('is_pb', required=True, type=bool)
dict_post_parser.add_argument('user_id', required=True, type=int)


# all arguments are required
