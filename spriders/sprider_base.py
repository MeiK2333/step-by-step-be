#coding=utf-8
import os
import sys
import time

import pymongo

AC = True
WA = False

class UserList(object):
    '''
    封装了查找和log操作的一个没有什么卵用的class
    '''

    def __init__(self, source):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['StepByStep']
        col = db['pool']
        self.source = source
        self.user_list = col.find({'source': source})
    
    def close(self):
        ''' 表面上看是关闭，其实就是打个log '''
        f = open(os.path.join(sys.path[0], 'log.txt'), 'a')
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + self.source + '\n')
        f.close()

def accepted(p_time):
    '''
    作用：判断指定的提交是否为AC（这里规定：提交时间后有'-Error'的为不正确，否则代表结果正确）
    示例：accepted('2015-09-28 17:14:02')
    '''
    return len(p_time) == 19

class BaseUser(object):
    '''
    封装了一些重复的操作
    '''

    def __init__(self, user):
        self.user = user
        self.user_name = user['user_name']

    def push(self, p_id, p_time, p_result):
        '''
        作用：将一个提交加入到该用户的提交数据中
        参数：p_id：题号 p_time：提交时间 p_result：提交状态（AC/WA）
        示例：User.push('1000', '2015-09-28 17:14:02', AC)
        '''
        if p_result: # 若要插入的是AC的数据
            if p_id in self.user['data'].keys(): # 若之前有过这个题目的状态
                if accepted(self.user['data'][p_id]): # 若之前这个题目已经AC过了
                    if p_time < self.user['data'][p_id]: # 若要插入的数据的提交时间早于已有数据
                        self.user['data'][p_id] = p_time
                    else:
                        pass
                else: # 若之前这个题目没有AC
                    self.user['data'][p_id] = p_time
            else: # 若之前没有这个题目的状态
                self.user['data'][p_id] = p_time
        else: # 若要插入的是WA的数据
            if p_id in self.user['data'].keys(): # 若之前有这个题目的状态
                if accepted(self.user['data'][p_id]): # 若之前的数据为AC
                    pass
                else: # 若之前的数据为WA
                    if p_time < self.user['data'][p_id]: # 若之前的数据早于已有数据
                        pass
                    else:
                        self.user['data'][p_id] = p_time + '-Error'
            else: # 若之前没有这个题目的状态
                self.user['data'][p_id] = p_time + '-Error'

    def save(self):
        ''' 保存数据 '''
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['StepByStep']
        col = db['pool']
        col.update({'_id': self.user['_id']}, self.user)

    def __str__(self):
        return self.user_name
