#coding=utf-8
from django.db import models
import pymongo
import urllib
import requests
import json

def getUserStepList_M(source, userName):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    user = db[source].find_one({"userName": userName})
    if user: #如果有这个用户
        return user['stepList'], user['allAc']
    return [], 0 #否则返回空列表

def getStepUser(stepId):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    step = db.stepList.find_one({"id": stepId})
    if step:
        return step['userList']
    return []

def getStepProblem(stepId):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    step = db.stepList.find_one({"id": stepId})
    if step:
        return step['problemList']
    return []

def getStep(stepId):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    step = db.stepData.find_one({"id": stepId})
    if step:
        return step
    return {}

def checkUser(username, source):
    if source == 'POJ':
        url = 'http://poj.org/userstatus?user_id=' + username
        try:
            data = urllib.urlopen(url).read()
            if '<title>Error</title>' in data:
                return False
            else:
                return username
        except:
            return False
    elif source == 'SDUT':
        url = "http://acm.sdut.edu.cn/StepByStepApi/getuserid.php?token=passwd&username=" + username
        try:
            data = urllib.urlopen(url).read()
            data = json.loads(data)
            if data['userid']:
                return data['userid']
            return False
        except:
            return False
    elif source == 'HDU':
        try:
            url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + username
            data = urllib.urlopen(url).read()
            if '<title>User Status - System Message</title>' in data:
                return False
            else:
                return username
        except:
            return False
    elif source == 'UVA':
        try:
            url = 'https://cn.vjudge.net/user/' + username
            data = requests.get(url)
            if data.status_code == 200:
                return username
            else:
                return False
        except:
            return False
    else:
        return False
