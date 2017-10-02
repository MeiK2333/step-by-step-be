#coding=utf-8
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

login_manager = LoginManager()
db = MongoEngine()

def create_app(Config):
    ''' 创建并初始化app '''
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    CSRFProtect(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .util import util as util_blueprint
    app.register_blueprint(util_blueprint, url_prefix='/util')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
