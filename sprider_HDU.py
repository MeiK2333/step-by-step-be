#coding=utf-8
from bs4 import BeautifulSoup
import urllib
import re
import json
import pymongo

def hdu_spider_func(userData):
    bottom = userData['bottom']
    acCount = userData['allAc']
    data = userData['data']
    user = userData['userName']
    while True:
        #利用poj的特性 每次从上次结束的地方开始查找即可
        url = 'http://acm.hdu.edu.cn/status.php?last=%s&user=%s'%(bottom, user)
        r = urllib.urlopen(url)
        soup = BeautifulSoup(r.read(), "html.parser")
        l = soup.find_all('td')
        #舍弃那些多余的td标签项
        l =  l[28:-4]
        #如果页面为空（没有题目状态） 则退出循环
        if len(l) <= 9:
            break
        #更新bottom
        bottom = str(l[0])[18:-5]
        print bottom
        #依次获取每条状态
        for i in range(len(l)/9)[::-1]:
            x = i * 9
            f = {}
            p = str(l[x+3])[40:-9]
            r = str(l[x+2])
            t = str(l[x+1])[4:-5]
            if len(r) == 42: #若结果为AC
                if p in data.keys(): #若之前已有数据
                    if len(data[p]) > 19: #判断之前为AC还是WA
                        data[p] = t
                        acCount += 1
                    else: #若之前已经AC，则不改变时间
                        continue
                else: #若为此题初次AC
                    data[p] = t
                    acCount += 1
            else: #结果为错误
                if p in data.keys(): #若之前有错误的结果，则更新时间
                    if len(data[p]) > 19:
                        data[p] = t + '-Error'
                    else: #若之前为AC，则忽视错误
                        continue
                else: #若之前没有过数据，则添加数据
                    data[p] = t + '-Error'
    userData['allAc'] = acCount
    userData['bottom'] = bottom
    col.update({"userName": user}, userData)

if '__main__' == __name__:
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStepData']
    col = db['HDU']
    userList = col.find()
    for i in userList:
        print i['userName']
        hdu_spider_func(i)