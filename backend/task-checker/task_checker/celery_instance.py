from celery import Celery


celery = Celery(
    'task_checker.tasks_flask',
    broker='pyamqp://guest:guest@rabbitmq:5672//',
    backend='rpc://',
)

celery.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    disable_rate_limits=True,
    ignore_result=True,
    task_result_expires=86400,
    timezone='UTC',
    enable_utc=True,
)

# Autodiscover tasks
celery.autodiscover_tasks(['task_checker.tasks_flask'], force=True)