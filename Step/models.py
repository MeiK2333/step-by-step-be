#coding=utf-8
from django.db import models
import pymongo
import xlrd
import sys

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

def readUserExcel(excelFile):
    path = sys.path[0]
    excel = open(path + '/upExcel.xlsx', 'wb+') #先将文件储存至本地
    for chunk in excelFile.chunks(): #以二进制的形式存入文件
        excel.write(chunk)
    excel.close()
    data = xlrd.open_workbook(path + '/upExcel.xlsx')
    table = data.sheets()[0] #解析excel文件
    classs = table.col_values(0)
    names = table.col_values(1)
    users = table.col_values(2)
    userList = []
    for i in range(len(users))[1:]:
        if isinstance(classs[i], float):
            classs[i] = str(int(classs[i]))
        if isinstance(names[i], float):
            names[i] = str(int(names[i]))
        if isinstance(users[i], float):
            users[i] = str(int(users[i]))
        userDict = {
            "userName": users[i],
            "name": names[i],
            "class": classs[i]
        }
        userList.append(userDict)
    return userList

def saveListExcel(excelFile, id):
    path = sys.path[0]
    excel = open(path + '/upExcel.xlsx', 'wb+') #先将文件储存至本地
    for chunk in excelFile.chunks(): #以二进制的形式存入文件
        excel.write(chunk)
    excel.close()
    data = xlrd.open_workbook(path + '/upExcel.xlsx')
    table = data.sheets()[0] #解析excel文件
    zxs = table.col_values(0)
    zts = table.col_values(1)
    tms = table.col_values(2)
    data = []
    for i in range(len(zxs)): #添加内容
        if isinstance(zxs[i], float):
            zxs[i] = str(int(zxs[i]))
        if isinstance(zts[i], float):
            zts[i] = str(int(zts[i]))
        if isinstance(tms[i], float):
            tms[i] = str(int(tms[i]))
        problemDict = {}
        if zxs[i]:
            problemDict['ZX'] = zxs[i]
        if zts[i]:
            problemDict['ZT'] = zts[i]
        problemDict['problem'] = tms[i]
        data.append(problemDict)

    ZX_len = 1
    ZT_len = 1
    for i in data[::-1]:
        if 'ZX' in i.keys():
            i['ZX_len'] = ZX_len
            ZX_len = 0
        ZX_len += 1
        if 'ZT' in i.keys():
            i['ZT_len'] = ZT_len
            ZT_len = 0
        ZT_len += 1
    
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client.StepByStepData
    lastData = db.stepList.find_one({"id": id}) #因为此函数经验证才能使用，因此这里直接使用id
    lastData['problemList'] = data
    db.stepList.update({"id": id}, lastData)

    return data