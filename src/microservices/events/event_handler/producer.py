import os

from aiokafka import AIOKafkaProducer

KAFKA_BROKERS = os.environ.get("KAFKA_BROKERS")


async def produce(topic: str, data: str):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKERS)
    await producer.start()
    try:
        await producer.send_and_wait(topic, data.encode())
    finally:
        await producer.stop()
