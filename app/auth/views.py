#coding=utf-8
from flask import render_template

from . import auth
from .forms import RegistrationForm, LoginForm


@auth.route('/')
def main():
    return 'auth'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'asdf'
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        '''
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        '''
        return form.username.data
    return render_template('auth/register.html', form=form)
