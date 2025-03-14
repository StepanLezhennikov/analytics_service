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
    TASK_CREATED: str = "task.create"
    TASK_UPDATED: str = "task.update"
    TASK_DELETED: str = "task.delete"
    PROJECT_CREATED: str = "project.create"
    PROJECT_DELETED: str = "project.delete"
    USER_ADDED: str = "user.add"
    USER_DELETED: str = "user.delete"


config = Config()
