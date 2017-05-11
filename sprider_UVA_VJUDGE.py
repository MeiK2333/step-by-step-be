#coding=utf-8
import os
import sys
import requests
import json
import time
import pymongo

url = 'https://cn.vjudge.net/status/data/'

def uva_vjudge_spider_func(userData):
    bottom = userData['bottom']
    acCount = userData['allAc']
    data = userData['data']
    user = userData['userName']
    start = 0
    draw = 1
    while True:
        #vjudge的返回数据已经是json格式
        #只需要获取直到列表为空或者获取的数据里有之前已经获取的为止
        postData = {
            #如果想获得vjudge的其他oj数据，只需要改动OJId即可
            "OJId": "UVA",
            "start": start,
            "length": 20,
            "un": user,
            "orderBy": "run_id",
            "res": 0,
            "draw": draw,
        }
        jsonData = json.loads(requests.post(url, data = postData).text)['data']
        #判断是否读取到末尾
        if not jsonData:
            break
        #更新bottom，初始化breakFlag
        if postData['start'] == 0:
            breakFlag = False
            userData['bottom'] = jsonData[0]['runId']
        for i in jsonData:
            p = str(i['probNum'])
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['time'] / 1000))
            #首先判断是否爬取到上次所在的地方
            if i['runId'] == int(bottom):
                breakFlag = True
                break
            #结果为AC
            if i['status'] == 'Accepted':
                #若之前已有此题数据
                if p in data.keys():
                    #判断之前为AC还是Error
                    #是Error则更新状态
                    #是AC则跳过
                    if len(data[p]) > 19:
                        data[p] = t
                        acCount += 1
                    else:
                        continue
                else:
                    data[p] = t
                    acCount += 1
            else:
                #状态为错误
                #若之前为错误，则更新时间
                #若之前没有数据，则添加数据
                #否则跳过
                if p in data.keys():
                    if len(data[p]) > 19:
                        data[p] = t + '-Error'
                    else:
                        continue
                else:
                    data[p] = t + '-Error'
        if breakFlag:
            break
        print start
        draw += 1
        start += 20

    userData['allAc'] = acCount
    col.update({"userName": user}, userData)

if '__main__' == __name__:
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStepData']
    col = db['UVA']
    userList = col.find()
    for i in userList:
        print i['userName']
        uva_vjudge_spider_func(i)
    f = open(os.path.join(sys.path[0], 'log.txt'), 'a')
    f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' UVA\n')
    f.close()
