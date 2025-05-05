import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.core.config import settings
from app.kafka_config.kafka_producer import kafka_producer
logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME)
    origins = ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = create_application()


@app.on_event("startup")
async def startup():
    logger.info("Starting Kafka producer and consumer...")
    try:
        await kafka_producer.start()
        logger.info("Kafka producer and consumer started.")
    except Exception as e:
        logger.error(f"Error starting Kafka producer or consumer: {e}")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Stopping Kafka producer and consumer...")
    try:
        await kafka_producer.stop()
        logger.info("Kafka producer and consumer stopped.")
    except Exception as e:
        logger.error(f"Error stopping Kafka producer or consumer: {e}")
