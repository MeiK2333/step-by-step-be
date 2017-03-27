#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from Org.models import Org
from Step.models import Step

#验证用户登录
def Login(request):
    if request.user.is_anonymous(): #验证当前登录状态
        if request.method == 'POST': #验证提交类型
            userName = request.POST.get('userName', '')
            passWord = request.POST.get('passWord', '')
            user = authenticate(username = userName, password = passWord) #验证登录
            if user:
                login(request, user) #登录此帐号
                orgId = user.last_name #获取组织id
                if not user.is_superuser: #获取所在组织信息
                    thisOrg = Org.objects.get(id = orgId)
                    orgName = thisOrg.name
                    shortName = thisOrg.shortName
                else:
                    orgName = 'SuperUser'
                    shortName = 'SuperUser'
                returnData = {
                    "status": True,
                    "data": {
                        "userName": user.username,
                        "nickName": user.first_name,
                        "orgId": user.last_name,
                        "orgName": orgName,
                        "shortName": shortName,
                    }
                }
                return JsonResponse(returnData)
            else:
                return JsonResponse({"status": False, "msg": "用户名或密码错误"})
        return render(request, 'Org/login.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    return JsonResponse({"status": False, "msg": "已经登录"})

#退出登录
def Logout(request):
    if request.user.is_anonymous():
        return JsonResponse({"status": False, "msg": "未登录"})
    logout(request)
    return JsonResponse({"status": True})

#创建Org管理员
def CreateOrgAdmin(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/CreateOrgAdmin.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    orgId = request.POST.get('orgId', '')
    userName = request.POST.get('userName', '')
    nickName = request.POST.get('nickName', '')
    passWord = request.POST.get('passWord', '')
    org = Org.objects.filter(id=int(orgId))
    if len(org) == 0: #判断指定id的Org是否存在
        return JsonResponse({"status": False, "msg": "Org不存在"})
    if len(User.objects.filter(username=userName)) > 0: #判断用户名是否已被使用
        return JsonResponse({"status": False, "msg": "用户名已被使用"})
    user = User()
    user.first_name = nickName
    user.username = userName
    user.set_password(passWord)
    user.last_name = orgId
    user.save()
    user = User.objects.get(username = userName) #重新获取一遍该用户数据
    returnData = {
        "status": True,
        "data": {
            "orgId": org[0].id,
            "userId": user.id,
            "userName": user.username,
            "nickName": user.first_name,
            "orgName": org[0].name,
            "shortName": org[0].shortName
        }
    }
    return JsonResponse(returnData)

#获得Org管理员列表
def GetOrgAdmin(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/GetOrgAdmin.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    orgId = request.POST.get('orgId', '')
    if orgId != '0': #不为0则查询指定Org
        users = User.objects.filter(last_name = str(orgId))
    else: #否则查询所有
        users = User.objects.all()
    orgs = Org.objects.all() #查询出所有的组织，用于管理员的对应
    org = {}
    for i in orgs:
        org[str(i.id)] = {"name": i.name, "shortName": i.shortName}
    userList = []
    for i in users:
        s = {}
        s['orgId'] = int(orgId)
        s['userId'] = i.id
        s['userName'] = i.username
        s['nickName'] = i.first_name
        s['orgName'] = org[i.last_name]['name']
        s['shortName'] = org[i.last_name]['shortName']
        userList.append(s)
    returnData = {
        "status": True,
        "count": len(users),
        "list": userList
    }
    return JsonResponse(returnData)

#修改管理员信息
def UpdateOrgAdmin(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/UpdateOrgAdmin.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    orgId = request.POST.get('orgId', '')
    userId = request.POST.get('userId', '')
    userName = request.POST.get('userName', '')
    nickName = request.POST.get('nickName', '')
    passWord = request.POST.get('passWord', '')
    if userName and len(User.objects.filter(username = userName)) > 0: #检查用户名
        return JsonResponse({"status": False, "msg": "用户名已被使用"})
    user = User.objects.filter(id = int(userId))
    if len(user) == 0: #没有查询结果
        return JsonResponse({"status": False, "msg": "没有这个用户"})
    user = user[0]
    org = Org.objects.filter(id = int(orgId))
    if len(org) == 0: #检查Org
        return JsonResponse({"status": False, "msg": "Org不存在"})
    org = org[0]
    if user.last_name != str(orgId):
        return JsonResponse({"status": False, "msg": "对应关系错误"})
    if nickName: #改变要修改的项
        user.first_name = nickName
    if passWord:
        user.set_password(passWord)
    if userName:
        user.username = userName
    user.save()
    returnData = {
        "status": True,
        "data": {
            "orgId": org.id,
            "userId": user.id,
            "userName": user.username,
            "nickName": user.first_name,
            "orgName": org.name,
            "shortName": org.shortName
        }
    }
    return JsonResponse(returnData)

#删除管理员
def DeleteOrgAdmin(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/DeleteOrgAdmin.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    orgId = request.POST.get('orgId', '')
    userId = request.POST.get('userId', '')
    user = User.objects.filter(id = int(userId)) #检查正确性
    if len(user) == 0:
        return JsonResponse({"status": False, "msg": "用户不存在"})
    user = user[0]
    if int(user.last_name) != int(orgId): #检查用户id与Orgid的对应
        return JsonResponse({"status": False, "msg": "对应关系错误"})
    User.objects.filter(id = int(userId)).delete()
    returnData = {
        "status": True,
        "data": {
            "userId": user.id,
            "userName": user.username,
            "nickName": user.first_name
        }
    }
    return JsonResponse(returnData)

#创建Org
def CreateOrg(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/CreateOrg.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    name = request.POST.get('name', '')
    shortName = request.POST.get('shortName', '')
    if len(Org.objects.filter(shortName = shortName)) > 0:
        return JsonResponse({"status": False, "msg": "此Org已存在"})
    org = Org() #新建
    org.name = name
    org.shortName = shortName
    org.save()
    org = Org.objects.get(shortName = shortName)
    returnData = {
        "status": True,
        "data": {
            "id": org.id,
            "name": org.name,
            "shortName": org.shortName
        }
    }
    return JsonResponse(returnData)

#修改Org
def UpdateOrg(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/UpdateOrg.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    id = request.POST.get('id', '')
    name = request.POST.get('name', '')
    shortName = request.POST.get('shortName', '')
    if shortName: #验证shortName是否重复
        org = Org.objects.filter(shortName = shortName)
        if len(org) > 0:
            return JsonResponse({"status": False, "msg": "shortName重复"})
    org = Org.objects.filter(id = id) #验证指定id的Org存在
    if len(org) == 0:
        return JsonResponse({"status": False, "msg": "Org不存在"})
    org = org[0]
    if name:
        org.name = name
    if shortName:
        org.shortName = shortName
    org.save()
    returnData = {
        "status": True,
        "data": {
            "id": org.id,
            "name": org.name,
            "shortName": org.shortName
        }
    }
    return JsonResponse(returnData)

#删除Org
def DeleteOrg(request):
    if request.method != 'POST': #检查请求类型
        return render(request, 'Org/DeleteOrg.html')
        return JsonResponse({"status": False, "msg": "请求类型必须为POST"})
    if request.user.is_anonymous(): #检查登录
        return JsonResponse({"status": False, "msg": "未登录"})
    if not request.user.is_superuser: #检查权限
        return JsonResponse({"status": False, "msg": "权限不足"})
    id = request.POST.get('id', '')
    org = Org.objects.filter(id = id)
    if len(org) == 0:
        return JsonResponse({"status": False, "msg": "Org不存在"})
    returnData = {
        "status": True,
        "data": {
            "id": org[0].id,
            "name": org[0].name,
            "shortName": org[0].shortName,
        }
    }
    org[0].delete()
    User.objects.filter(last_name = id).delete()
    return JsonResponse(returnData)