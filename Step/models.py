#coding=utf-8
from django.db import models
import pymongo

class Step(models.Model):
    title = models.CharField(max_length = 60)
    userCount = models.IntegerField()
    problemCount = models.IntegerField()
    allAcCount = models.IntegerField()
    orgId = models.IntegerField()
    source = models.CharField(max_length = 30)

def Step_save(step):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.insert(step)

def Step_Update(id, step):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.update({"id": id}, step)

def Step_Delete(id):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    db.stepList.remove({"id": id})

def StepList_Update(id, userName, nickName, _class, userId):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    step = db.stepList.find_one({"id": id}) #因为之前对sqlite中的数据进行了验证，因此这里默认有这条数据
    userData = {
        "userId": userId,
        "userName": userName,
        "name": nickName,
        "class": _class
    }
    step['userList'].append(userData) #将当前用户添加至列表中
    db.stepList.update({"id": id}, step)

def StepUser_Update(source, id, userName): #更新用户信息
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    stepUser = db[source].find_one({"userName": userName})
    if stepUser: #若此用户之前存在
        if not id in stepUser['stepList']: #若此计划之前不存在
            stepUser['stepList'].append(id)
        db[source].update({"userName": userName}, stepUser)
    else: #否则插入新的数据
        stepUser = {
            "userName": userName,
            "bottom": 0,
            "allAc": 0,
            "data": {},
            "stepList": [id]
        }
        db[source].insert(stepUser)

def StepList_Delete(id, userName, userId):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    step = db.stepList.find_one({"id": id}) #默认能拿到数据
    if step['userList'][userId-1]['userId'] == userId and step['userList'][userId-1]['userName'] == userName: #判断userName与userId对应
        del step['userList'][userId-1]
        db.stepList.update({"id": id}, step) #更新数据
        return True
    return False

def StepUser_Delete(source, id, userName):
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    stepUser = db[source].find_one({"userName": userName})
    if stepUser:
        stepUser['stepList'].remove(id) #此函数应该在验证后执行，因此默认计划存在
        db[source].update({"userName": userName}, stepUser)
