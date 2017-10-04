#coding=utf-8
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm, TokenForm
from ..models import db, User, generate_email_token, check_email_token
from ..email import send_email

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
        user.email = form.token.data.split('/')[0]
        user.save()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/token/', methods=['GET', 'POST'])
def token_email():
    form = TokenForm()
    if form.validate_on_submit():
        tk = generate_email_token(form.email.data)
        send_email(form.email.data, 'Token', 'auth/token', token='/'.join([form.email.data, tk]))
        return redirect(url_for('auth.register'))
    return render_template('auth/token.html', form=form)
