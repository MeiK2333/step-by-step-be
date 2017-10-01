#coding=utf-8
from config import Config
from app import create_app

app = create_app()
app.config.from_object(Config)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
