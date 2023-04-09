import os
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


if __name__ == "__main__":
    mpt('/api/user', get)
    mpt('/api/user/1', get)
    mpt('/api/user/2', get)
    mpt('/api/user/dhjsvdn', get)
    mpt('/api/post', post, {'nick': 'abc 123',
                            'email': 'admin228@gmail.com',
                            'password': 'abc123'})
    mpt('/api/post', post, {'nick': 'abc 123',
                            'email': 'admin227@gmail.com',
                            'password': 'abc123'})
