#coding=utf-8
from . import main
from flask import render_template
from ..models import Info, Plan, User, PlanData

@main.route('/')
def index():
    users = User.objects(display=True).all()
    return render_template('main/main.html', users=users)

@main.route('/guide/')
def guide():
    return render_template('guide.html')

@main.route('/u/<name>')
def plan_list(name):
    plans = Plan.objects(root=name).all()
    plans = sorted(plans, key=lambda d : d.sort_id)
    return render_template('main/plan_list.html', plans=plans)

@main.route('/u/<name>/<int:sort_id>')
def step(name, sort_id):
    return render_template('main/step.html', name=name, sort_id=sort_id)
