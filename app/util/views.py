#coding=utf-8
import os
from config import Config

from flask import jsonify, request
import xlrd

from . import util
from .. import csrf
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

@util.route('/parser_excel/', methods=['POST'])
@csrf.exempt
def post_parser_excel():
    ''' 解析Excel文件 '''
    file_ = request.files['file']
    if not file_ or not file_.filename.split('.')[1] == 'xlsx':
        return jsonify({'msg': u'文件格式错误'})

    file_.save(os.path.join(Config.UPLOAD_FOLDER, 'upload.xlsx'))

    data = xlrd.open_workbook(os.path.join(Config.UPLOAD_FOLDER, 'upload.xlsx'))
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    excel_data = {
        'rows': nrows,
        'cols': ncols,
    }
    excel_list =[]
    for rownum in range(nrows):
        row = table.row_values(rownum)
        excel_list.append(row)
    excel_data['data'] = excel_list
    return jsonify(excel_data)
