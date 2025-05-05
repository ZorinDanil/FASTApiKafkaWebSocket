import asyncio
import logging

from app.api import router
from app.core.config import settings
from app.kafka_config.kafka_consumer import kafka_consumer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    application.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = create_application()


@app.on_event("startup")
async def startup():
    logger.info("Starting Kafka consumer...")
    try:
        await kafka_consumer.start()
        asyncio.create_task(kafka_consumer.consume())
        logger.info("Kafka consumer started.")
    except Exception as e:
        logger.error(f"Error starting Kafka consumer: {e}")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Stopping Kafka consumer...")
    try:
        await kafka_consumer.stop()
        logger.info("Kafka consumer stopped.")
    except Exception as e:
        logger.error(f"Error stopping Kafka consumer: {e}")
