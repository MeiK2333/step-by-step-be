#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from Org.models import Org
from Step.models import Step, Step_save, Step_Update, Step_Delete, StepUser_Update

def index(request):
    return render(request, 'Step/index.html')

#新建计划
def CreateStep(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Step/CreateStep.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    orgId = request.POST.get('orgId', '')
    if not request.user.is_superuser: #检查权限
        if request.user.last_name != orgId: #对应org的管理员
            return JsonResponse({"status": False, "msg": "权限不足"})
    title = request.POST.get('title', '')
    source = request.POST.get('source', '')
    if source != 'SDUT' and source != 'POj' and source != 'HDU':
        return JsonResponse({"status": False, "msg": "source错误"})
    if not (orgId and title and source): #检验信息填写
        return JsonResponse({"status": False, "msg": "信息不足"})
    org = Org.objects.filter(id = int(orgId))
    if len(org) == 0: #检验org合法
        return JsonResponse({"status": False, "msg": "org不存在"})
    step = Step()
    step.title = title
    step.source = source
    step.userCount = 0
    step.problemCount = 0
    step.allAcCount = 0
    step.orgId = int(orgId)
    step.save()
    step = Step.objects.filter(title = title) #获取刚刚储存的数据
    for i in step: #因为其他项有可能相同，因此获得最后一个
        s = i
    returnData = {
        "status": True,
        "data": {
            "orgId": s.orgId,
            "id": s.id,
            "title": s.title,
            "source": s.source
        }
    }
    step_M = {
        "orgId": s.orgId,
        "id": s.id,
        "title": s.title,
        "source": s.source,
        "userList": [],
        "problemList": []
    }
    Step_save(step_M) #在mongo数据库中储存
    return JsonResponse(returnData)

#修改计划
def UpdateStep(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Step/UpdateStep.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    orgId = request.POST.get('orgId', '')
    if not request.user.is_superuser: #检查权限
        if request.user.last_name != orgId:
            return JsonResponse({"status": False, "msg": "权限不足"})
    id = request.POST.get('id', '')
    title = request.POST.get('title', '')
    source = request.POST.get('source', '')
    step = Step.objects.filter(id = int(id))
    if len(step) == 0:
        return JsonResponse({"status": False, "msg": "Step不存在"})
    step = step[0]
    if step.orgId != int(orgId): #检查匹配
        return JsonResponse({"status": False, "msg": "orgId与id不匹配"})
    if title:
        step.title = title
    if source:
        step.source = source
    step.save()
    step = Step.objects.get(id = int(id))
    returnData = {
        "status": True,
        "data": {
            "orgId": step.orgId,
            "id": step.id,
            "title": step.title,
            "source": step.source
        }
    }
    step_M = {
        "orgId": step.orgId,
        "id": step.id,
        "title": step.title,
        "source": step.source
    }
    Step_Update(step.id, step_M)
    return JsonResponse(returnData)

#删除计划
def DeleteStep(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Step/DeleteStep.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    orgId = request.POST.get('orgId', '')
    if not request.user.is_superuser: #检查权限
        if request.user.last_name != orgId:
            return JsonResponse({"status": False, "msg": "权限不足"})
    id = request.POST.get('id', '')
    step = Step.objects.filter(id = int(id))
    if len(step) == 0: #检查存在
        return JsonResponse({"status": False, "msg": "Step不存在"})
    step = step[0]
    if step.orgId != int(orgId): #检查匹配
        return JsonResponse({"status": False, "msg": "orgId与id不匹配"})
    returnData = {
        "status": True,
        "data": {
            "orgId": step.orgId,
            "id": step.id,
            "title": step.title,
            "source": step.source
        }
    }
    Step_Delete(step.id)
    step.delete()
    return JsonResponse(returnData)

#为计划添加用户
def AddStepUser(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Step/AddStepUser.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    orgId = request.POST.get('orgId', '')
    if not request.user.is_superuser: #检查权限
        if request.user.last_name != orgId:
            return JsonResponse({"status": False, "msg": "权限不足"})
    id = request.POST.get('id', '')
    userName = request.POST.get('userName', '')
    nickName = request.POST.get('nickName', '')
    _class = request.POST.get('class', '')
    if not (userName or nickName or _class):
        return JsonResponse({"status": False, "msg": "信息不足"})
    step = Step.objects.filter(orgId = int(orgId))
    if len(step) == 0:
        return JsonResponse({"status": False, "msg": "Org不存在"})
    step = step[0]
    #此处还没写完，应该为调用models中的update，然后返回数据