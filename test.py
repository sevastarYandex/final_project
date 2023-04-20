"""py-file with test function"""


from requests import get, put, post, delete
from pprint import pprint
from data.constant import API_SITE


def mpt(par, fun, params=None):
    """test function, returns json-response,
    par - api-request (kind a 'object/id' or 'object' (object - user, word or dict))
    fun - requests function (get, delete, post or put)
    params - params of post/put request"""
    if params is None:
        return fun(API_SITE + par).json()
    return fun(API_SITE + par, **{'json': params}).json()
