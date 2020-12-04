import time

from celery import shared_task

from source.spider.sdut_problems import sdut_problems


@shared_task
def sdut_problems_task():
    sdut_problems()
