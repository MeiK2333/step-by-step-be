#coding=utf-8
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from ..models import db, User


@auth.route('/')
@login_required
def main():
    return render_template('main.html')

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(user_name=form.user_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('auth/login.html', form=form)

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.user_name = form.user_name.data
        user.nick_name = form.user_name.data
        user.password = form.password.data
        user.save()
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
