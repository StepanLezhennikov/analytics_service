import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.services.kafka_consumer import KafkaConsumerService

kafka_consumer_service = KafkaConsumerService()

logger = logging.getLogger("kafka_consumer")

logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kafka Consumer...")
    await kafka_consumer_service.start_consuming()

    asyncio.create_task(kafka_consumer_service.consume())
    yield

    logger.info("Stopping Kafka Consumer...")
    await kafka_consumer_service.stop_consuming()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
