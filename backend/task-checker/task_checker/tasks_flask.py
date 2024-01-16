import uuid
import json
from json.decoder import JSONDecodeError

from confluent_kafka import Consumer, TopicPartition
from celery import Celery

from task_checker.models import Item
from task_checker.database import db


celery = Celery('task_checker.tasks_flask', broker='pyamqp://guest:guest@rabbitmq:5672//')

group_id = f"myapp_{uuid.uuid4()}"
KAFKA_BOOTSTRAP_SERVERS = 'kafka_task:9092'

@celery.task(queue='queue_for_task2')
def save_message_to_database_async(value):
    from task_checker.app import app

    with app.app_context():
        try:
            print("Processing message:", value)

            title = value.get('title')
            description = value.get('description')

            new_item = Item(title=title, description=description)
            db.session.add(new_item)
            db.session.commit()

            print("Message saved to the database:", value)

        except Exception as e:
            print(f"Error processing message: {e}")

@celery.task(queue='queue_for_task2')
def consume_kafka_messages(topic):
    print("Starting celery kafka messages")
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

    print("Consumer Configuration:", consumer)
    
    print("topic=================", topic)
    tp = TopicPartition(topic, 0)
    consumer.assign([tp])
    print("tp=================", tp)
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                print("msg is None", msg)
                break
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            try:
                string_message = msg.value().decode('utf-8')
                print("String received",string_message)

                message_data = json.loads(string_message)
                print('Received message:', message_data)      

                save_message_to_database_async.delay(message_data)  

            except JSONDecodeError as e:
                print('Error decoding JSON: {}'.format(e))
                print('Problematic message: {}'.format(msg.value().decode('utf-8')))

    except KeyboardInterrupt:
        print("Received keyboard interrupt")
    finally:
        consumer.close()















import asyncio
from task_checker.consumers import consume_messages

event = asyncio.Event()


@celery.task(queue='queue_for_task2')
def async_subscribe(subject):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume_messages(subject, event))

event.set()