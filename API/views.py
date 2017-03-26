#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Org.models import Org

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