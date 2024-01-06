from confluent_kafka import Consumer, KafkaException
from celery import Celery
from flask import jsonify


celery = Celery('tasks', broker='pyamqp://guest:guest@rabbitmq:5672//')
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9093'

@celery.task
def consume_kafka_messages(topic):
    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'flask_consumer_group',
        'auto.offset.reset': 'earliest'
    }

    print(topic, "topic=================================")
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
        msg = consumer.poll(1.0)
        if msg is not None and not msg.error():
            received_message = msg.value().decode('utf-8')
            return jsonify({'status': 'Message consumed successfully', 'message': received_message})

    finally:
        consumer.close()

    return jsonify({'status': 'No message available'})
    # consumer_conf = {
    #     'bootstrap.servers': 'kafka_task:9093',
    #     'group.id': 'task_consumer_group',
    #     'auto.offset.reset': 'earliest'
    # }

    # consumer = Consumer(consumer_conf)
    # consumer.subscribe([topic])

    # try:
    #     while True:
    #         msg = consumer.poll(1.0)
    #         if msg is None:
    #             continue
    #         if msg.error():
    #             if msg.error().code() == KafkaException._PARTITION_EOF:
    #                 continue
    #             else:
    #                 print(msg.error())
    #                 break
    #         print('Received message: {}'.format(msg.value().decode('utf-8')))
    # finally:
    #     consumer.close()