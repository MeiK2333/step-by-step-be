#coding=utf-8
import json

import requests

from sprider_base import AC, WA, BaseUser, UserList

def sprider_sdut(user):
    print user
    to_uid_url = 'http://acm.sdut.edu.cn/StepByStepApi/getuserid.php?token=passwd&username=' + user.user_name
    uid = json.loads(requests.get(to_uid_url).text)['userid']
    data_url = 'http://acm.sdut.edu.cn/StepByStepApi/useraccept.php?token=passwd&userid=' + uid
    data = json.loads(requests.get(data_url).text)['problem']
    for i in data:
        user.push(i['problem_id'], i['sub_time'], AC)
    user.save()

if __name__ == '__main__':
    Users = UserList('SDUT')
    for i in Users.user_list:
        u = BaseUser(i)
        sprider_sdut(u)
    Users.close()
