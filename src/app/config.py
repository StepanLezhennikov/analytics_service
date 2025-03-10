import os
import logging
from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

logging.basicConfig(level=logging.ERROR)


class Config(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    KAFKA_TOPIC_CREATE_TASK: str = "create_task"

    class Topics(str, Enum):
        CREATE_TASK = "create_task"


config = Config()
