from __future__ import absolute_import
import os
import logging
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')

app = Celery('student_management')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

logging.basicConfig(filename='celery.log', level=logging.INFO)

@app.task(bind=True)
def debug_task(self):
    print(f"request: {self.request!r}")
