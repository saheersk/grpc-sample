import uuid

from confluent_kafka import Consumer, TopicPartition
from celery import Celery

from task_checker.models import Item
from task_checker.database import db


celery = Celery('task_checker.tasks_flask', broker='pyamqp://guest:guest@rabbitmq:5672//')

group_id = f"myapp_{uuid.uuid4()}"
KAFKA_BOOTSTRAP_SERVERS = 'kafka_task:9092'


@celery.task(queue='queue_for_task2')
def save_message_to_database_async(value):
    print("Processing message:", value)

    title = value.get('title')
    description = value.get('description')

    new_item = Item(title=title, description=description)
    db.session.add(new_item)
    db.session.commit()

    print("Message saved to the database:", value)

@celery.task(queue='queue_for_task2')
def consume_kafka_messages(topic):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

    tp = TopicPartition(topic, 0)
    consumer.assign([tp])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                print("No more messages. Stopping.")
                break
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            message_value = msg.value().decode('utf-8')
            print('Received message: {}'.format(message_value))

            save_message_to_database_async.delay(message_value)

    except KeyboardInterrupt:
        print("Received keyboard interrupt")
    finally:
        consumer.close()


