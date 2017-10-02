#coding=utf-8
from config import Config
from app import create_app, db, login_manager, CSRFProtect

app = create_app(Config)

if __name__ == '__main__':
    app.jinja_env.cache = None
    app.run(debug=True, port=5000, host='0.0.0.0')
