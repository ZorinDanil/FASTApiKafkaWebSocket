import json
import os
import asyncio
import logging
from typing import Optional
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')


class KafkaProducer:
    """
    Asynchronous Kafka producer.

    Initializes a Kafka producer with the specified bootstrap servers.
    """

    def __init__(self) -> None:
        """
        Initialize Kafka producer.

        Args:
            bootstrap_servers (Optional[str]): Kafka bootstrap servers.
                Defaults to environment variable KAFKA_BOOTSTRAP_SERVERS or
                'kafka:9092'.
        """
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        self.producer: Optional[AIOKafkaProducer] = None

    async def __aenter__(self):
        """
        Async context manager entry.

        Starts the Kafka producer.

        Returns:
            self
        """
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit.

        Stops the Kafka producer.
        """
        await self.stop()

    async def start(self):
        """
        Start the Kafka producer.
        """
        if self.producer is None:
            loop = asyncio.get_running_loop()
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                loop=loop
            )
            await self.producer.start()
            logger.info("Kafka producer started.")

    async def stop(self):
        """
        Stop the Kafka producer.
        """
        if self.producer:
            await self.producer.stop()
            self.producer = None
            logger.info("Kafka producer stopped.")

    async def encode_message(self, message: dict):
        return json.dumps(message).encode('utf-8')

    async def send(self, topic: str, message: dict):
        """
        Send a message to a Kafka topic.

        Args:
            topic (str): Kafka topic.
            message (dict): Message to be sent.

        Raises:
            Exception: If the producer is not initialized.
        """
        if self.producer is None:
            raise Exception("Producer is not initialized")
        logger.info(f"Sending message to Kafka topic '{topic}': {message}")
        encoded_message = await self.encode_message(message)
        await self.producer.send(topic, encoded_message)
        logger.info("Message sent successfully.")


kafka_producer = KafkaProducer()
