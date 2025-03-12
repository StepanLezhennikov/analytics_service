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
    logger.info("Starting Kafka Consumer...")
    await kafka_consumer_service.start_consuming()

    asyncio.create_task(kafka_consumer_service.consume())
    yield

    logger.info("Stopping Kafka Consumer...")
    await kafka_consumer_service.stop_consuming()


app = FastAPI(lifespan=lifespan)

app.container = container


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
