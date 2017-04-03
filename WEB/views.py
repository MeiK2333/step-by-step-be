#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, 'WEB/index.html')

def step(request, stepId):
    return render(request, 'WEB/step.html', {'stepId': stepId})

def admin(request):
    if request.user.is_anonymous(): #检查登录
        return HttpResponseRedirect('/')
    if not request.user.is_superuser: #检查权限
        orgId = request.user.last_name
    else:
        orgId = request.GET.get('orgId', '1')
    return render(request, 'WEB/admin.html', {"orgId": orgId})

def user(request):
    source = request.GET.get('source', '')
    userName = request.GET.get('userName', '')
    if not (source and userName):
        return HttpResponseRedirect('/')
    return render(request, 'WEB/user.html', {"source": source, "userName": userName})