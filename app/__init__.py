#coding=utf-8
from flask import Flask

def create_app():
    ''' 创建并初始化app '''
    app = Flask(__name__)

    from .util import util as util_blueprint
    app.register_blueprint(util_blueprint, url_prefix='/util')

    return app
