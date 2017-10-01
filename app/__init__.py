#coding=utf-8
#from flask import Flask
from flask_wtf.csrf import CsrfProtect

from flask import Flask

def create_app():
    ''' 创建并初始化app '''
    app = Flask(__name__)

    CsrfProtect(app)

    from .util import util as util_blueprint
    app.register_blueprint(util_blueprint, url_prefix='/util')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
