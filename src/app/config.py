import os
import logging
from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

logging.basicConfig(level=logging.ERROR)


class Config(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


class TOPICS(str, Enum):
    TASK_CREATED: str = "task_created"
    TASK_UPDATED: str = "task_updated"
    TASK_DELETED: str = "task_deleted"
    PROJECT_CREATED: str = "project_created"
    PROJECT_UPDATED: str = "project_updated"
    PROJECT_DELETED: str = "project_deleted"


config = Config()
