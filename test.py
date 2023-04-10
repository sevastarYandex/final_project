from requests import get, put, post, delete
from pprint import pprint

necc = 'http://127.0.0.1:8080'


def mpt(par, fun, params=None, if_p=True):
    if params is None:
        params = {}
    if params:
        params = {'json': params}
    if not if_p:
        return fun(necc + par, **params).json()
    pprint(fun(necc + par, **params).json())
    print('-' * 30)

#
# def user_api():
#     mpt('/api/user', get)
#     mpt('/api/user/1', get)
#     mpt('/api/user/2', get)
#     mpt('/api/user/dhjsvdn', get)
#     mpt('/api/user', post, {'nick': 'abc 123',
#                             'email': 'admin228@gmail.com',
#                             'password': 'abc123'})
#     mpt('/api/user', get)
#     mpt('/api/user', post, {'nick': 'abc 123',
#                             'email': 'admin123@gmail.com',
#                             'password': 'abc123'})
#     mpt('/api/user', get)
#     mpt('/api/user/sfsdf', put, {'nick': 'abc 123',
#                                  'email': 'admin123@gmail.com',
#                                  'password': 'abc123'})
#     mpt('/api/user', get)
#     mpt('/api/user/3', put, {'nick': 'abc 123',
#                              'email': 'admin123@gmail.com',
#                              'password': 'abc123'})
#     mpt('/api/user', get)
#     mpt('/api/user/2', put, {'nick': 'abc 123',
#                              'email': 'admin228@gmail.com',
#                              'password': 'abc123'})
#     mpt('/api/user', get)
#     mpt('/api/user/2', put, {'nick': 'abc 123',
#                              'email': 'admin227@gmail.com',
#                              'password': 'abc1234567'})
#     mpt('/api/user', get)
#     mpt('/api/user/3', delete)
#     mpt('/api/user', get)
#     mpt('/api/user/sdfsd', delete)
#     mpt('/api/user', get)
#     mpt('/api/user/2', delete)
#     mpt('/api/user', get)
#
#
# def word_api():
#     mpt('/api/word', get)
#     mpt('/api/word/1', get)
#     mpt('/api/word/2', get)
#     mpt('/api/word/dhjsvdn', get)
#     mpt('/api/word', post, {'word': 'sm_word',
#                             'translation_list': 'какое-то слово',
#                             'user_id': 2,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word', post, {'word': 'word',
#                             'translation_list': 'слово',
#                             'user_id': 1,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word', post, {'word': 'not a word',
#                             'translation_list': 'не слово',
#                             'user_id': 1,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word/sfsdf', put, {'word': 'not a word',
#                             'translation_list': 'не слово',
#                             'user_id': 1,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word/3', put, {'word': 'not a word',
#                             'translation_list': 'не слово',
#                             'user_id': 1,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word/2', put, {'word': 'not a word',
#                             'translation_list': 'не слово',
#                             'user_id': 2,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word/2', put, {'word': 'a word',
#                             'translation_list': 'не слово',
#                             'user_id': 1,
#                             'is_public': True})
#     mpt('/api/word', get)
#     mpt('/api/word/2', put, {'word': 'not a word',
#                              'translation_list': 'не слово',
#                              'user_id': 1,
#                              'is_public': False})
#     mpt('/api/word', get)
#     mpt('/api/word/3', delete)
#     mpt('/api/word', get)
#     mpt('/api/word/sdfsd', delete)
#     mpt('/api/word', get)
#     mpt('/api/word/2', delete)
#     mpt('/api/word', get)


if __name__ == "__main__":
    # user_api()
    # word_api()
    pass
