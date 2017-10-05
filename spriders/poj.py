#coding=utf-8
import requests
from bs4 import BeautifulSoup
from sprider_base import AC, WA, BaseUser, UserList

class POJUser(BaseUser):
    '''
    为加速爬虫速度，减少查询次数，保存bottom数据以从上次结束的地方继续
    '''

    def __init__(self, user):
        super(POJUser, self).__init__(user)
        if not 'bottom' in self.user.keys():
            self.user['bottom'] = 0
        self.bottom = user['bottom']

    def sprider(self):
        print self.user_name
        user = self.user_name
        bottom = self.user['bottom']
        while True:
            #利用poj的特性 每次从上次结束的地方开始查找即可
            url = 'http://poj.org/status?user_id=%s&bottom=%s'%(user, bottom)
            r = requests.get(url).text
            soup = BeautifulSoup(r, "html.parser")
            l = soup.find_all('td')
            #舍弃那些多余的td标签项
            l =  l[23:]
            #如果页面为空（没有题目状态） 则退出循环
            if len(l) == 0:
                break
            #更新bottom
            bottom = str(l[0])[4:-5]
            print bottom
            #依次获取每条状态
            for i in range(len(l)/9)[::-1]:
                x = i * 9
                f = {}
                p = str(l[x+2])[30:-9]
                r = str(l[x+3])
                t = str(l[x+8])[4:-5]
                self.push(p, t, AC if len(r) == 43 else WA)
        self.user['bottom'] = bottom


if __name__ == '__main__':
    Users = UserList('POJ')
    for i in Users.user_list:
        u = POJUser(i)
        u.sprider()
        u.save()
    Users.close()
        