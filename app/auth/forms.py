#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import Email, EqualTo, Length, Regexp, Required
from ..models import db, User, check_email_token

class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[
            Required(message=u'这个字段是必填的'), Length(3, 16, message=u'用户名长度在3-16位之间')
        ])
    password = PasswordField('Password', validators=[Required(message=u'这个字段是必填的'), Length(1, 64)])
    submit = SubmitField('Login')

    def validate_user_name(self, field):
        if not User.objects(user_name=field.data).first():
            raise ValidationError(u'用户名不存在')

class RegistrationForm(FlaskForm):
    token = StringField('Token', validators=[
        Required(message=u'这个字段是必填的')])
    user_name = StringField('Username', validators=[
        Required(message=u'这个字段是必填的'), Length(3, 16, message=u'长度在3-16位之间')])
    password = PasswordField('Password', validators=[
        Required(message=u'这个字段是必填的'), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField('Confirm', validators=[Required(message=u'这个字段是必填的')])
    submit = SubmitField('Register')

    def validate_token(self, field):
        try:
            email, token = field.data.split('/')
            if not check_email_token(email, token):
                raise ValidationError(u'Token无效或已过期')
        except:
            raise ValidationError(u'Token错误')

    def validate_user_name(self, field):
        if User.objects(user_name=field.data).first():
            raise ValidationError(u'用户名已经被占用')

class TokenForm(FlaskForm):
    email = StringField('Emain', validators=[
        Required(message=u'这个字段是必填的'), Email(message=u'格式错误')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.objects(email=field.data).first():
            raise ValidationError(u'邮箱已经被使用')