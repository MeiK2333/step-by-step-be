#coding=utf-8
import re
import pymongo
import json
import urllib

def sdut_spider_func(userData):
    uid = userData['userName']
    url = 'http://acm.sdut.edu.cn/StepByStepApi/useraccept.php?token=passwd&userid=' + uid
    date = json.loads(urllib.urlopen(url).read())['problem']
    status = {}
    acCount = 0
    for i in date: #调用SDUTAPI，只能获得正确的题目数据
        status[i['problem_id']] = i['sub_time']
        acCount += 1
    userData['data'] = status
    userData['allAc'] = acCount
    col.update({"userName": uid}, userData)

if __name__ == '__main__':
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStepData']
    col = db['SDUT']
    userList = col.find()
    for i in userList:
        print i['userName']
        sdut_spider_func(i)
