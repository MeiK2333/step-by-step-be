#coding=utf-8
import sqlite3
import os
import sys
import pymongo

def main(id, source, title, problemCount):
    print id, source, title
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStepData']
    col = db['stepList']
    step = col.find_one({"id": id})
    problemList = step['problemList'] #huo qu ti mu lie biao
    users = step['userList']
    userList = []
    allAc = 0
    data = {}
    for user in users: #yi ci wei mei ge user sheng cheng
        print user
        userData = db[source].find_one({"userName": user['userName']})
        pbs = {}
        acCount = 0
        for i in problemList:
            pb = i['problem']
            if pb in userData['data'].keys():
                if len(userData['data'][pb]) > 19: #WA
                    pbs[pb] = userData['data'][pb][:10] + '-Error'
                else:
                    pbs[pb] = userData['data'][pb][:10]
                    acCount += 1
        user['count'] = acCount
        data[user['userName']] = pbs
        allAc += acCount
    stepData = {
        "id": id,
        "source": source,
        "title": title,
        "problemList": problemList,
        "problemCount": allAc,
        "userList": users,
        "data": data
    }
    db.stepData.update({"id": id}, stepData)


if __name__ == '__main__':
    path = sys.path[0]
    cor = sqlite3.connect(path + '/db.sqlite3')
    cursor = cor.execute('SELECT id, source, title, problemCount from Step_step')
    stepList = cursor.fetchall()
    for step in stepList:
        main(step[0], step[1], step[2], step[3])
    f = open(os.path.join(sys.path[0], 'log.txt'), 'a')
    f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' conversion\n')
    f.close()
