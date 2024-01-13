from django.conf import settings

from confluent_kafka import Producer
from nats.aio.client import Client as NATS
import asyncio


KAFKA_BOOTSTRAP_SERVERS = 'kafka_task:9092'


def produce_kafka_message(topic, message):
        print("produce======================")
        producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

        print("producer==============", producer)

        def delivery_report(err, msg):
            print(msg, 'delivery report')
            if err is not None:
                print('Message delivery failed: {}'.format(err))
            else:
                print('Message delivered to {} {}'.format(msg.topic(), msg.partition()))

        print(f"Producing message to topic: {topic}, message: {message}")
        producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
        producer.flush()


async def verify_message(subject):
   nc = NATS()
   await nc.connect(servers=["nats://localhost:4222"])
   async def message_received(msg):
       print(f"Verified message: {msg.data}")
   await nc.subscribe(subject, cb=message_received)
   await asyncio.sleep(1)
   await nc.close()

async def publish_message(subject, message):
    nats_client = NATS()

    try:
        print("nats producer========", message)
        # connection = await nats_client.connect(servers=["nats://localhost:4222"])
        connection = await nats_client.connect(servers=["nats://demo.nats.io:4222"], tls=False)

        print("Connection========", connection)
        # Ensure message is encoded to bytes
        message_bytes = message.encode("utf-8")

        print("nats producer bytes========", message_bytes)


        # Publish the message
        publisher = await nats_client.publish(subject, message_bytes)

        # Check if the message was successfully published
        publish_status = await publisher.ack
        print(f"Publish status: {publish_status}")

    except Exception as e:
        print(f"Error publishing message: {e}")
    finally:
        await nats_client.close()



# asyncio.run(verify_message(subject))
