#coding=utf-8
from . import admin
from flask import request, render_template, redirect
from flask_login import login_required
from config import Config

@admin.route('/')
@login_required
def main():
    return render_template('admin/index.html', sources=Config.SOURCES)