from datetime import datetime

from pydantic import BaseModel


class Topic(BaseModel):
    created_at: datetime
    project_id: int


class ProjectCreated(Topic):
    tasks: list[int]
    members: list[int]


class ProjectDeleted(Topic):
    pass


class TaskCreated(Topic):
    task_id: int
    status: str


class TaskUpdated(Topic):
    task_id: int
    user_id: int
    status: str
    task_started_time: datetime


class TaskDeleted(Topic):
    task_id: int


class UserCreated(Topic):
    user_id: int


class UserDeleted(Topic):
    user_id: int
