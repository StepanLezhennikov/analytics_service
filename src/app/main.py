import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.containers import Container
from app.infrastructure.services.kafka_consumer import KafkaConsumerService

kafka_consumer_service = KafkaConsumerService()

container = Container()

container.wire(packages=[__name__, "app.infrastructure.services"])

logger = logging.getLogger("main")

logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with KafkaConsumerService() as kafka_consumer:
        asyncio.create_task(kafka_consumer.consume())
        yield


app = FastAPI(lifespan=lifespan)

app.container = container


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
