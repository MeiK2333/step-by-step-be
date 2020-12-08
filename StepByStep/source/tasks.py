from celery import shared_task

from source.spider.sdut_problems import sdut_problems
from source.spider.sdut_solutions import sdut_solutions
from source.spider.poj_problems import poj_problems


@shared_task
def sdut_problems_task():
    sdut_problems()


@shared_task
def poj_problems_task():
    poj_problems()


@shared_task
def sdut_solutions_task():
    sdut_solutions()
