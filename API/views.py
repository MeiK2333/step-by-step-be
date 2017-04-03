#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Org.models import Org
from Step.models import Step
from API.models import *

#查询所有Org
def GetOrgList(request):
    orgs = Org.objects.all()
    orgList = []
    for i in orgs:
        s = {}
        s['id'] = i.id
        s['name'] = i.name
        s['shortName'] = i.shortName
        orgList.append(s)
    returnData = {
        "status": True,
        "count": len(orgs),
        "list": orgList
    }
    return JsonResponse(returnData)

#获取指定Org的Step列表
def GetStepList(request):
    orgId = request.GET.get('orgId', '')
    try: #判断输入是否为数字
        orgId = int(orgId)
        org = Org.objects.filter(id = orgId)
        if len(org) == 0:
            return JsonResponse({"status": False, "msg": "Org不存在"})
        step = Step.objects.filter(orgId = int(orgId))
        stepList = []
        for i in step:
            s = {}
            s['id'] = i.id
            s['title'] = i.title
            s['userCount'] = i.userCount
            s['problemCount'] = i.problemCount
            s['allAcCount'] = i.allAcCount
            s['source'] = i.source
            stepList.append(s)
        returnData = {
            "status": True,
            "count": len(step),
            "orgId": org[0].id,
            "orgName": org[0].name,
            "shortName": org[0].shortName,
            "list": stepList
        }
        return JsonResponse(returnData)
    except: #如果不是数字，则返回所有列表
        step = Step.objects.all()
        stepList = []
        for i in step:
            s = {}
            s['id'] = i.id
            s['title'] = i.title
            s['userCount'] = i.userCount
            s['problemCount'] = i.problemCount
            s['allAcCount'] = i.allAcCount
            s['source'] = i.source
            stepList.append(s)
        returnData = {
            "status": True,
            "count": len(step),
            "list": stepList
        }
        return JsonResponse(returnData)

#获取某人参加的所有计划
def GetUserStepList(request):
    source = request.GET.get('source', '')
    userName = request.GET.get('userName', '')
    if source and userName:
        stepList, allAc = getUserStepList_M(source, userName)
        return JsonResponse({"status": True, "stepList": stepList, "allAc": allAc})
    return JsonResponse({"status": False, "msg": "信息不足"})

#获取某计划的参与用户
def GetStepUser(request):
    stepId = request.GET.get('stepId', '')
    if stepId:
        userList = getStepUser(int(stepId))
        return JsonResponse({"status": True, "userList": userList})
    return JsonResponse({"status": False, "msg": "信息不足"})

#获取某计划的题目
def GetStepProblem(request):
    stepId = request.GET.get('stepId', '')
    if stepId:
        problemList = getStepProblem(int(stepId))
        return JsonResponse({"status": True, "problemList": problemList})
    return JsonResponse({"status": False, "msg": "信息不足"})

#获取某计划的内容
def GetStep(request):
    stepId = request.GET.get('stepId', '')
    if stepId:
        data = getStep(int(stepId))
        data['status'] = True
        if '_id' in data.keys():
            del data['_id']
        return JsonResponse(data)
    return JsonResponse({"status": False, "msg": "信息不足"})

#获取某人在某计划中的做题情况
def GetUserStep(request):
    stepId = request.GET.get('stepId', '')
    userName = request.GET.get('userName', '')
    if stepId and userName:
        data = getStep(int(stepId))
        if not data or not userName in data['data'].keys():
            return JsonResponse({"status": False, "msg": "无数据"})
        returnData = {
            "status": True,
            "userName": userName,
            "problemList": data['problemList'],
            "data": data['data'][userName],
            "title": data['title']
        }
        return JsonResponse(returnData)
    return JsonResponse({"status": False, "msg": "信息不足"})

#检查用户是否存在
def CheckUser(request):
    userName = request.GET.get('userName', '')
    source = request.GET.get('source', '')
    if source and userName:
        user = checkUser(userName, source)
        if not user:
            return JsonResponse({"status": False, "msg": "验证失败"})
        returnData = {
            "status": True,
            "userName": userName
        }
        if source == 'SDUT':
            returnData['uid'] = user
        return JsonResponse(returnData)
    return JsonResponse({"status": False, "msg": "信息不足"})