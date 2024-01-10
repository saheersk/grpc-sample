from confluent_kafka import Producer


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