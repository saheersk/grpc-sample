from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task.settings')

app = Celery('task')
app.conf.enable_utc = False
app.conf.update(
 task_routes={
     'task1': {'queue': 'queue_for_task1'},
 },
 timezone='Asia/Kolkata'
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry = True
# app.conf.broker_connection_retry_on_startup = True 

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(['task_service.api'], force=True)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')