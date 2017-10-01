#coding=utf-8
from config import Config

from flask import jsonify, request

from . import util
from .model import check_user_exist


@util.route('/')
def main():
    ''' main '''
    return 'Hello World!'

@util.route('/check_user/', methods=['GET', 'POST'])
def check_user():
    ''' 检查提交的账号是否存在 '''
    query_source = request.form.get('source', None)
    query_user = request.form.get('user_name', None)
    if (request.method != 'POST') or (not query_source in Config.SOURCES) or (query_user is None):
        return jsonify({
            u'请求示例': {
                'method': 'POST',
                'source': '/'.join(Config.SOURCES),
                'user_name': 'user_name'
            }
        })

    exist = check_user_exist(query_user, query_source)
    if exist is None:
        return jsonify({'msg': u'内部错误'})
    return jsonify({
        'user_name': query_user,
        'source': query_source,
        'exist': check_user_exist(query_user, query_source)
    })
