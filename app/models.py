#coding=utf-8
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager

class User(UserMixin, db.Document):
    ''' 管理员（域） '''
    user_name = db.StringField(max_length=50) # 用户名
    password_hash = db.StringField(max_length=128) # 密码（hash后）
    nick_name = db.StringField(max_length=128)
    display = db.BooleanField(default=False) # 是否可见
    plan_cnt = db.IntField(default=0) # 已创建的计划数量

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.objects(id=id).first()

class Pool(db.Document):
    ''' 更新池 '''
    root = db.StringField(max_length=50) # 所属域
    user_id = db.StringField(max_length=50) # 该用户唯一标识
    source = db.StringField(max_length=50) # 该用户所在的平台
    data = db.DictField() # 该用户的提交信息

class Info(db.Document):
    ''' 用户信息 '''
    root = db.StringField(max_length=50) # 所属域
    user_id = db.StringField(max_length=50) # 该用户唯一标识
    nick_name = db.StringField(max_length=50) # 该用户昵称
    class_ = db.StringField(max_length=50) # 该用户所在班级
    user_list = db.DictField() # 账号列表

class Plan(db.Document):
    ''' 计划 '''
    root = db.StringField(max_length=50) # 所属域
    name = db.StringField(max_length=100) # 计划名
    sort_id = db.IntField() # 显示时排序的凭证
    display = db.BooleanField(default=True) # 是否显示

    plan_body = db.ListField() # 计划内容主体
    plan_user = db.ListField() # 计划参与用户
