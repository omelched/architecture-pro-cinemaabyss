import os

from aiokafka import AIOKafkaConsumer

KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS')

async def consume():
    consumer = AIOKafkaConsumer('movie-events', 'user-events', 'payment-events', bootstrap_servers=KAFKA_BROKERS)
    await consumer.start()

    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        await consumer.stop()