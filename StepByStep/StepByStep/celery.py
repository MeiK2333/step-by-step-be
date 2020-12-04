import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StepByStep.settings")
app = Celery("StepByStep")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
