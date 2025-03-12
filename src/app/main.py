import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.services.kafka_consumer import KafkaConsumerService

kafka_consumer_service = KafkaConsumerService()

logger = logging.getLogger("main")

logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with KafkaConsumerService() as kafka_consumer:
        asyncio.create_task(kafka_consumer.consume())
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
