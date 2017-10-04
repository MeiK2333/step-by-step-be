#coding=utf-8
import json
from config import Config

import requests


def check_user_exist(user_name, source):
    ''' 检查某平台的某用户是否存在 '''
    if not source in Config.SOURCES:
        return False

    if source == 'POJ':
        url = 'http://poj.org/userstatus?user_id=' + user_name
        try:
            data = requests.get(url).text
            if '<title>Error</title>' in data:
                return False
            else:
                return True
        except:
            return None
    elif source == 'SDUT':
        url = "http://acm.sdut.edu.cn/StepByStepApi/getuserid.php?token=passwd&username=" + user_name
        try:
            data = requests.get(url).text
            data = json.loads(data)
            if data['userid']:
                return True
            return False
        except:
            return None
    elif source == 'HDU':
        try:
            url = 'http://acm.hdu.edu.cn/userstatus.php?user=' + user_name
            data = requests.get(url).text
            if '<title>User Status - System Message</title>' in data:
                return False
            else:
                return True
        except:
            return False
    elif source == 'VJ':
        try:
            url = 'https://vjudge.net/user/' + user_name
            data = requests.get(url)
            if data.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    else:
        return False
