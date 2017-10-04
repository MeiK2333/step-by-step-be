#coding=utf-8

class Config:
    SECRET_KEY = 'QAQrz'

    SOURCES = [
        'SDUT', 'HDU', 'POJ', 'VJ'
    ]

    MONGODB_DB = 'StepByStep'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017

    MAIL_SERVER = 'pop.stumail.sdut.edu.cn'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '111057201@stumail.sdut.edu.cn'
    MAIL_PASSWORD = '111057201'
    FLASKY_MAIL_SUBJECT_PREFIX = 'StepByStep'
    FLASKY_MAIL_SENDER = '111057201@stumail.sdut.edu.cn'
    FLASKY_ADMIN = 'StepByStep'

    UPLOAD_FOLDER = 'app/static/file/'