#coding=utf-8
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from . import db, login_manager

class User(UserMixin, db.Document):
    ''' 管理员（域） '''
    user_name = db.StringField(max_length=50) # 用户名
    password_hash = db.StringField(max_length=128) # 密码（hash后）
    nick_name = db.StringField(max_length=128)
    display = db.BooleanField(default=True) # 是否可见
    plan_cnt = db.IntField(default=0) # 已创建的计划数量
    email = db.StringField(max_length=128)

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
    user_name = db.StringField(max_length=50) # 该用户在对应平台的账号
    source = db.StringField(max_length=50) # 该用户所在的平台
    data = db.DictField() # 该用户的提交信息

class Info(db.Document):
    ''' 用户信息 '''
    root = db.StringField(max_length=50) # 所属域
    user_id = db.StringField(max_length=50) # 该用户唯一标识
    plan_list = db.ListField(default=[]) # 该用户参与的计划列表

class PlanData(db.Document):
    ''' 计划的数据 '''
    root = db.StringField()
    name = db.StringField()
    source = db.StringField()
    sort_id = db.IntField()
    p_id = db.IntField()
    plan_body = db.ListField()
    plan_user = db.ListField()
    plan_data = db.DictField()

class Plan(db.Document):
    ''' 计划 '''
    root = db.StringField(max_length=50) # 所属域
    name = db.StringField(max_length=100) # 计划名
    source = db.StringField(max_length=50) # 计划所在平台
    sort_id = db.IntField() # 显示时排序的凭证
    p_id = db.IntField() # 用户反向查找时的凭证
    display = db.BooleanField(default=True) # 是否显示

    plan_body = db.ListField(default=[]) # 计划内容主体
    '''
    [
        {
			"ZX" : 专项名,
			"ZX_len" : 专项题目个数,
            "ZT" : 专题名,
			"ZT_len" : 专题题目个数,
			"problem" : 题号（字符串格式）,
        }
    ]
    '''
    plan_user = db.ListField(default=[]) # 计划参与用户
    '''
    [
        {
            'id': 唯一标识,
            'user_name': 用户名,
            'name': 姓名,
            'class': 班级,
        }
    ]
    '''
    plan_user_cnt = db.IntField(default=0) # 用户个数
    plan_body_cnt = db.IntField(default=0) # 题目个数

    def add_user(self, id_, user_name_, name_, class_):
        u = {
            'id': id_,
            'user_name': user_name_,
            'name': name_,
            'class': class_,
        }
        for i in self.plan_user:
            if i['id'] == u['id']:
                i.update(u)
                break
        else:
            self.plan_user.append(u)
        self.plan_user_cnt = len(self.plan_user)

        self.add_pool(id_, user_name_)
        self.add_info(id_)

    def add_pool(self, id_, user_name_):
        source = self.source
        root = self.root
        pool = Pool.objects(root=root, user_id=id_, source=source).first()
        if pool:
            pool.user_name = user_name_
        else:
            pool = Pool(
                root=root, user_id=id_, user_name=user_name_, source=source
            )
        pool.save()

    def add_info(self, id_):
        root = self.root
        info = Info.objects(root=root, user_id=id_).first()
        if info is None:
            info = Info(root=root, user_id=id_)
        p_id = self.p_id
        if not p_id in info.plan_list:
            info.plan_list.append(p_id)
        info.save()

    def del_user(self, id_):
        cnt = 0
        for i in self.plan_user:
            if id_ == i['id']:
                self.plan_user.pop(cnt)
                break
            cnt += 1
        self.plan_user_cnt = len(self.plan_user)
        self.del_info(id_)

    def del_info(self, id_):
        root = self.root
        info = Info.objects(root=root, user_id=id_).first()
        if info:
            info.plan_list.remove(self.p_id)
        info.save()

def generate_email_token(email, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'email': email})

def check_email_token(email, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('email') != email:
        return False
    return True