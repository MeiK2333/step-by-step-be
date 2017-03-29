#coding=utf-8
from django.db import models
import pymongo

def getUserStepList_M(source, userName):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    user = db[source].find_one({"userName": userName})
    if user: #如果有这个用户
        return user['stepList']
    return [] #否则返回空列表

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