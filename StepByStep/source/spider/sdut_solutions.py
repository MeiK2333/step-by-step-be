import requests

import datetime
from source.models import Problem, Solution, SourceUser
from django.contrib.auth.models import User


def user_solutions(source_user: SourceUser):
    userid = int(source_user.username)
    print(f'get solutions by {userid}')
    last_solution_id = source_user.last_solution_id
    url = f'https://acm.sdut.edu.cn/StepByStepApi/solutions.php?userid={userid}&solution_id={last_solution_id}'
    resp = requests.get(url).json()
    last_id = last_solution_id
    for row in resp:
        problem, _ = Problem.objects.get_or_create(
            problem_id=row['problem_id'],
            source=source_user.source,
            defaults={'title': 'unknown problem', 'link': 'https://acm.sdut.edu.cn/onlinejudge3/'}
        )
        solution_id = row['solution_id']
        if last_id < int(solution_id):
            last_id = int(solution_id)
        Solution.objects.update_or_create(
            source_user=source_user,
            run_id=row['solution_id'],
            defaults={
                'problem': problem,
                'result': row['result'],
                'language': row['pro_lang'],
                'time_used': int(row['take_time']),
                'memory_used': int(row['take_memory']),
                'length': int(row['code_length']),
                'submitted_at': row['sub_time']
            }
        )
    source_user.last_solution_id = last_id
    source_user.save()
    return resp


def sdut_solutions():
    # 获取最近 90 天有过登录的用户
    end_date = datetime.datetime.now() + datetime.timedelta(days=10)
    start_date = datetime.datetime.now() - datetime.timedelta(days=90)
    users = User.objects.filter(last_login__range=(start_date, end_date))
    source_users = []
    for user in users:
        for source_user in SourceUser.objects.filter(user=user):
            source_users.append(source_user)

    for source_user in source_users:
        try:
            user_solutions(source_user)
        except Exception as ex:
            print(repr(ex))
            print(ex)
