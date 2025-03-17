import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.containers import Container
from app.core.services.consumer import ConsumerService
from app.infrastructure.api.rest.controllers import api

kafka_consumer_service = ConsumerService()

container = Container()

container.wire(packages=[__name__, "app.infrastructure.services"])
container.wire(packages=[__name__, "app.infrastructure.api.rest.v1"])

logger = logging.getLogger("main")

logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ConsumerService() as kafka_consumer:
        asyncio.create_task(kafka_consumer.consume())
        yield


app = FastAPI(lifespan=lifespan)

app.container = container

app.include_router(api)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
