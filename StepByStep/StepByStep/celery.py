import os

from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StepByStep.settings")

app = Celery("StepByStep")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(
    CELERYBEAT_SCHEDULE={
        "sdut-problem": {
            "task": "source.tasks.sdut_problems_task",
            "schedule": timedelta(hours=12),
        }
    }
)

app.autodiscover_tasks()
