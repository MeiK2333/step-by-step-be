#coding=utf-8
from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     ValidationError)
from wtforms.validators import Email, EqualTo, Length, Regexp, Required

class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[
            Required(), Length(1, 64)
        ])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if field.data == 'a':
            raise ValidationError(u'用户名不能为a')
'''
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
'''