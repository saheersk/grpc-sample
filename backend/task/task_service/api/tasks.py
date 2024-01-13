from celery import Celery
from asgiref.sync import async_to_sync 
import asyncio

from .producers import produce_kafka_message, publish_message


celery = Celery('task_service.api.tasks', broker='pyamqp://guest:guest@rabbitmq:5672//')
sync_publish_message = async_to_sync(publish_message)

@celery.task(queue='queue_for_task1')
def async_produce_kafka_message(topic, message):
    print("======================Celery async produce=======================")
    produce_kafka_message(topic, message)

@celery.task(queue='queue_for_task1')
def async_produce_nat(subject, message):
    print("======================Celery nats produce=======================", subject, message)
    # async_to_sync(publish_message)(subject, message)
    asyncio.run(publish_message("your_subject", "your_message"))
    # asyncio.ensure_future(publish_message(subject, message))