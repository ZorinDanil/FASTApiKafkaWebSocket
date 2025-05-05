import os
import asyncio
import json

from typing import Optional
import uuid

from aiokafka import AIOKafkaConsumer

from app.api.deps import get_session
from app.models import Profile

import logging

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
TOPIC_NAME = os.getenv('KAFKA_TOPIC', 'user_events')

logger = logging.getLogger(__name__)


class KafkaConsumer:
    """
    Asynchronous Kafka Consumer.

    Initializes a Kafka Consumer with the specified bootstrap servers.
    """

    def __init__(self) -> None:
        """
        Initialize Kafka consumer.

        Args:
            bootstrap_servers (Optional[str]): Kafka bootstrap servers.
                Defaults to environment variable KAFKA_BOOTSTRAP_SERVERS or
                'kafka:9092'.
        """
        self.bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        self.consumer: Optional[AIOKafkaConsumer] = None
        
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
        if self.consumer is None:
            loop = asyncio.get_running_loop()
            self.consumer = AIOKafkaConsumer(
                TOPIC_NAME,
                bootstrap_servers=self.bootstrap_servers,
                loop=loop
            )
            await self.consumer.start()
            logger.info("Kafka cosumer started.")

    async def stop(self):
        """
        Stop the Kafka producer.
        """
        if self.consumer:
            await self.consumer.stop()
            self.consumer = None
            logger.info("Kafka consumer stopped.")
            
    async def consume(self):
        logger.info("Starting to consume messages...")
        async for msg in self.consumer:
            event = json.loads(msg.value.decode("utf-8"))
            event_type = event["type"]
            user_data = event["user"]
            logger.info(f"Consumed event: {event_type} for user: {user_data}")

            if event_type == "user_created":
                await self.handle_user_created(user_data)

    @staticmethod
    async def handle_user_created(user_data: dict):
        async for session in get_session():
            async with session.begin():
                user_id = user_data.get("id")
                profile = Profile(
                    user_id=str(user_id),
                    id=uuid.uuid4()
                )
                session.add(profile)
                await session.commit()
                await session.refresh(profile)
                logger.info(f"Profile created for user: {user_id}")


kafka_consumer = KafkaConsumer()
