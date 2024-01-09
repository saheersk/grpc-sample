
from .producers import produce_kafka_message

from celery import Celery


celery = Celery('task_service.api.tasks', broker='pyamqp://guest:guest@rabbitmq:5672//')

@celery.task(queue='queue_for_task1')
def async_produce_kafka_message(topic, message):
    print("======================Celery async produce=======================")
    produce_kafka_message(topic, message)