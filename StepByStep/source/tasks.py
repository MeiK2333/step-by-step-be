import time

from celery import shared_task


@shared_task
def check():
    for i in range(10):
        print(i)
        time.sleep(i)
    return True
