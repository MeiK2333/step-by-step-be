#coding=utf-8
from . import api
from flask import request, jsonify
from flask_login import login_required, current_user
from ..models import User, Plan, PlanData
from config import Config
import json

@api.route('/this/nick_name/', methods=['GET'])
@login_required
def get_this_nick_name():
    ''' 返回域的名称 '''
    return jsonify({'nick_name': current_user.nick_name})

@api.route('/this/nick_name/', methods=['POST'])
@login_required
def post_this_nick_name():
    ''' 修改域的名称 '''
    new_nick_name = request.form.get('nick_name', current_user.nick_name)
    user = User.objects(id=current_user.id).first()
    user.nick_name = new_nick_name
    user.save()
    return jsonify({'nick_name': user.nick_name})

@api.route('/this/plan_list/', methods=['GET'])
@login_required
def get_this_plan_list():
    ''' 获取计划列表 '''
    plans = Plan.objects(root=current_user.user_name).all()
    r_data = []
    for plan in plans:
        p_data = {
            'sort_id': plan.sort_id,
            'name': plan.name,
            'source': plan.source,
            'root': plan.root,
            'plan_body_cnt': plan.plan_body_cnt,
            'plan_user_cnt': plan.plan_user_cnt,
        }
        r_data.append(p_data)
    return jsonify(r_data)

@api.route('/this/plan_list/', methods=['POST'])
@login_required
def post_this_plan_list():
    ''' 新建一个计划 '''
    plan = Plan()
    plan.name = request.form.get('name', '-')
    plan.source = request.form.get('source', None)
    if not plan.source in Config.SOURCES:
        return jsonify({'msg': u'source错误'})
    plan.root = current_user.user_name
    plan.sort_id = current_user.plan_cnt
    plan.p_id = plan.sort_id
    plan.save()

    user = User.objects(id=current_user.id).first()
    user.plan_cnt += 1
    user.save()

    return jsonify({'name': plan.name, 'source': plan.source, 'sort_id': plan.sort_id})

@api.route('/this/plan_pos/', methods=['POST'])
@login_required
def this_plan_pos():
    ''' 将计划移位 '''
    pos = request.form.get('pos', None)
    sort_id = request.form.get('sort_id', None)
    if pos is None or sort_id is None:
        return jsonify({'msg': u'参数错误'})
    if int(pos) < 0 or int(pos) >= current_user.plan_cnt:
        return jsonify({'msg': u'越界错误'})
    plan1 = Plan.objects(sort_id=int(sort_id)).first()
    if not plan1:
        return jsonify({'msg': u'计划不存在'})
    plan2 = Plan.objects(sort_id=int(pos)).first()
    if plan2:
        tmp = plan1.sort_id
        plan1.sort_id = plan2.sort_id
        plan2.sort_id = tmp
        plan1.save()
        plan2.save()
    else:
        plan1.sort_id = pos
        plan1.save()
    return jsonify({'name': plan1.name, 'source': plan1.source, 'sort_id': plan1.sort_id})

@api.route('/this/plan/name/', methods=['POST'])
@login_required
def post_this_plan_name():
    ''' 修改计划名称 '''
    sort_id = request.form.get('sort_id', None)
    name = request.form.get('name', None)
    if sort_id is None or name is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    plan.name = name
    plan.save()
    return jsonify({'name': plan.name, 'source': plan.source, 'sort_id': plan.sort_id})

@api.route('/this/plan/', methods=['DELETE'])
@login_required
def delete_this_plan():
    ''' 删除指定的计划'''
    sort_id = request.form.get('sort_id', None)
    if sort_id is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    plan.delete()
    return jsonify({'code': 0})

@api.route('/this/plan/user_list/', methods=['POST'])
@login_required
def post_this_plan_user_list():
    ''' 为计划添加一个用户 '''
    sort_id = request.form.get('sort_id', None)
    user_name = request.form.get('user_name', None)
    user_id = request.form.get('user_id', None)
    class_ = request.form.get('class', None)
    name = request.form.get('name', None)
    if sort_id is None or user_id is None or user_name is None or class_ is None or name is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    plan.add_user(user_id, user_name, name, class_)
    plan.save()
    return jsonify({'code': 0})

@api.route('/this/plan/user_list/', methods=['DELETE'])
@login_required
def delete_this_plan_user_list():
    ''' 为计划删除一个用户 '''
    sort_id = request.form.get('sort_id', None)
    user_id = request.form.get('user_id', None)
    if sort_id is None or user_id is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    plan.del_user(user_id)
    plan.save()
    return jsonify({'code': 0})

@api.route('/this/plan/user_list/', methods=['GET'])
@login_required
def this_plan_user_list():
    ''' 获取计划的用户列表 '''
    sort_id = request.args.get('sort_id', None)
    if sort_id is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    return jsonify(plan.plan_user)

@api.route('/this/plan/body/', methods=['GET'])
@login_required
def this_plan_body():
    ''' 获取计划的题目 '''
    sort_id = request.args.get('sort_id', None)
    if sort_id is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    return jsonify(plan.plan_body)

@api.route('/this/plan/body/', methods=['POST'])
@login_required
def post_this_plan_body():
    ''' 上传计划题目 '''
    sort_id = request.form.get('sort_id', None)
    plan_body = request.form.get('plan_body', None)
    if sort_id is None or plan_body is None:
        return jsonify({'msg': u'参数错误'})
    plan = Plan.objects(sort_id=int(sort_id)).first()
    if not plan:
        return jsonify({'msg': u'计划不存在'})
    plan_body = json.loads(plan_body)
    plan.plan_body = plan_body
    plan.plan_body_cnt = len(plan_body)
    plan.save()
    return jsonify({'code': 0})

@api.route('/plan/data/<name>/<int:sort_id>/')
def get_plan_data(name, sort_id):
    plan_data = PlanData.objects(root=name, sort_id=sort_id).first()
    return jsonify(plan_data)