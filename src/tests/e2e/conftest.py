from datetime import datetime, timedelta

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import TOPICS, TaskStatus


@pytest.fixture
def project_create_dict():
    def _factory(i: int) -> dict:
        return {
            "project_id": i,
            "tasks": [i],
            "members": [i],
            "created_at": datetime.now() - timedelta(days=i),
        }

    return _factory


@pytest.fixture
def task_create_dict():
    def _factory(i: int) -> dict:
        return {
            "task_id": i,
            "project_id": i,
            "status": TaskStatus.BACKLOG.value,
            "deadline": datetime.now() - timedelta(days=i),
            "created_at": datetime.now() - timedelta(days=i),
        }

    return _factory


@pytest.fixture
def user_create_dict():
    def _factory(i: int) -> dict:
        return {
            "user_id": i,
            "project_id": i,
            "created_at": datetime.now() - timedelta(days=i),
        }

    return _factory


@pytest.fixture
def task_update_dict():
    def _factory(task_id: int, project_id: int, user_id: int) -> dict:
        return {
            "task_id": task_id,
            "project_id": project_id,
            "user_id": user_id,
            "status": TaskStatus.DONE.value,
            "deadline": datetime.now() - timedelta(days=task_id),
            "task_started_time": datetime.now() - timedelta(days=2 * task_id),
            "created_at": datetime.now() - timedelta(days=task_id),
        }

    return _factory


@pytest.fixture
async def create_projects(db: AsyncIOMotorDatabase, project_create_dict):
    async def _factory(count: int):
        collection = db.get_collection(TOPICS.PROJECT_CREATED.value)
        projects = [project_create_dict(i) for i in range(1, count + 1)]
        await collection.insert_many(projects)
        return projects

    return _factory


@pytest.fixture
async def delete_project(db: AsyncIOMotorDatabase):
    async def _factory(i: int):
        collection = db.get_collection(TOPICS.PROJECT_DELETED.value)
        project = {"project_id": i, "created_at": datetime.now()}
        await collection.insert_one(project)

        return project

    return _factory


@pytest.fixture
async def create_tasks(db: AsyncIOMotorDatabase, task_create_dict):
    async def _factory(count: int):
        collection = db.get_collection(TOPICS.TASK_CREATED.value)
        tasks = [task_create_dict(i) for i in range(1, count + 1)]
        await collection.insert_many(tasks)
        return tasks

    return _factory


@pytest.fixture
async def delete_task(db: AsyncIOMotorDatabase):
    async def _factory(i: int):
        collection = db.get_collection(TOPICS.TASK_DELETED.value)
        task = {"project_id": i, "task_id": i, "created_at": datetime.now()}
        await collection.insert_one(task)

        return task

    return _factory


@pytest.fixture
async def create_users(db: AsyncIOMotorDatabase, user_create_dict):
    async def _factory(count: int):
        collection = db.get_collection(TOPICS.USER_CREATED.value)
        users = [user_create_dict(i) for i in range(1, count + 1)]
        await collection.insert_many(users)
        return users

    return _factory


@pytest.fixture
async def delete_user(db: AsyncIOMotorDatabase):
    async def _factory(i: int):
        collection = db.get_collection(TOPICS.USER_DELETED.value)
        user = {"project_id": i, "task_id": i, "created_at": datetime.now()}
        await collection.insert_one(user)

        return user

    return _factory


@pytest.fixture
async def finish_task(db: AsyncIOMotorDatabase, task_update_dict):
    async def _factory(task_id: int, project_id: int, user_id: int):
        collection = db.get_collection(TOPICS.TASK_UPDATED.value)
        task = task_update_dict(task_id, project_id, user_id)
        await collection.insert_one(task)
        print("UPDATED TASK", task)
        return task

    return _factory
