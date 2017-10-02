#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import Email, EqualTo, Length, Regexp, Required
from ..models import db, User

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
    user_name = StringField('Username', validators=[
        Required(message=u'这个字段是必填的'), Length(3, 16, message=u'长度在3-16位之间')])
    password = PasswordField('Password', validators=[
        Required(message=u'这个字段是必填的'), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField('Confirm', validators=[Required(message=u'这个字段是必填的')])
    submit = SubmitField('Register')

    def validate_user_name(self, field):
        if User.objects(user_name=field.data).first():
            raise ValidationError(u'用户名已经被占用')
