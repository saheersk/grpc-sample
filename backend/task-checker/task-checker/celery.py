from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        broker_url=app.config['CELERY_BROKER_URL'],
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        disable_rate_limits=True,
        ignore_result=True,
        task_result_expires=86400,  # 1 day in seconds
        timezone='UTC',
        enable_utc=True,
        app='flask'  # Unique identifier for this worker
    )
    return celery