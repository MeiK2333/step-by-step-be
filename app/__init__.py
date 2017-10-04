#coding=utf-8
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_mail import Mail

login_manager = LoginManager()
db = MongoEngine()
mail = Mail()
csrf = CSRFProtect()

def create_app(Config):
    ''' 创建并初始化app '''
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)
    csrf.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .util import util as util_blueprint
    app.register_blueprint(util_blueprint, url_prefix='/util')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
