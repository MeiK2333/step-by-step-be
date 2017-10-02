#coding=utf-8
from . import main
from flask import render_template
from ..models import Info, Plan

@main.route('/')
def index():
    return render_template('guide.html')

@main.route('/guide/')
def guide():
    return render_template('guide.html')

@main.route('/user/')
def user():
    info = Info()
    info.class_ = 'rj'
    info.user_id = '15110572001'
    info.nick_name = 'MeiK'
    info.user_list = {
        "VJ": "MeiK",
        "SDUT": "15110572001",
        "HDU": "MeiK",
        "POJ": "MeiK",
    }
    info.save()
    return 'success'

@main.route('/step/')
def step():
    plan = Plan()
    plan.root = 'MeiK'
    plan.name = 'step_1'
    plan.sort_id = 0
    plan.plan_body = [
        {
            "1": 1,
        },
        {
            "2": 2,
        }
    ]
    plan.plan_user = [
        '15110572001'
    ]
    plan.save()
    return 'success'
