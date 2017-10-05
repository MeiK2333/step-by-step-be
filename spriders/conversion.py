#coding=utf-8
import os
import sys
import time

import pymongo


def main(step):
    source = step['source']
    title = step['name']
    print source, title

    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStep']

    problem_list = step['plan_body'] # 获取题目列表
    users = step['plan_user']
    userList = []
    allAc = 0
    data = {}
    for user in users:
        userData = db['pool'].find_one({"user_name": user['user_name'], 'source': source})
        pbs = {}
        acCount = 0
        for i in problem_list:
            pb = i['problem']
            if pb in userData['data'].keys():
                if len(userData['data'][pb]) > 19: #WA
                    pbs[pb] = userData['data'][pb][:10] + '-Error'
                else:
                    pbs[pb] = userData['data'][pb][:10]
                    acCount += 1
        user['count'] = acCount
        data[user['user_name']] = pbs
        allAc += acCount
    stepData = {
        "root": step['root'],
        "source": source,
        "name": title,
        "plan_body": problem_list,
        "plan_user": users,
        "plan_data": data,
        'sort_id': step['sort_id'],
        'p_id': step['p_id'],
    }
    old_data = db['plan_data'].find_one({"root": step['root'], 'p_id': step['p_id']})
    if old_data:
        db['plan_data'].update({"root": step['root'], 'p_id': step['p_id']}, stepData)
    else:
        db['plan_data'].insert(stepData)


if __name__ == '__main__':
    client = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
    db = client['StepByStep']
    col = db['plan']
    step_list = col.find()
    for step in step_list:
        main(step)
    f = open(os.path.join(sys.path[0], 'log.txt'), 'a')
    f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' conversion\n')
    f.close()
