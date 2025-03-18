import os
import logging
from enum import Enum

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

logging.basicConfig(level=logging.ERROR)


class Config(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE")


class TOPICS(str, Enum):
    TASK_CREATED: str = "task.create"
    TASK_UPDATED: str = "task.update"
    TASK_DELETED: str = "task.delete"
    PROJECT_CREATED: str = "project.create"
    PROJECT_DELETED: str = "project.delete"
    USER_CREATED: str = "user.create"
    USER_DELETED: str = "user.delete"


class TaskStatus(str, Enum):
    BACKLOG: str = "BACKLOG"
    RUNNING: str = "RUNNING"
    DONE: str = "DONE"
