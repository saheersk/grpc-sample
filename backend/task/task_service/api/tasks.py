from celery import shared_task
from .producers import produce_kafka_message

@shared_task
def async_produce_kafka_message(topic, message):
    print("======================Celery async produce=======================")
    produce_kafka_message(topic, message)