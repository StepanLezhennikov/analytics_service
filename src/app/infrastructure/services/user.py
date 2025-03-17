from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS
from app.core.interfaces.services.user import UserServiceInterface
from app.core.interfaces.repositories.mongo_repo import MongoRepositoryInterface


class UserService(UserServiceInterface):
    def __init__(
        self,
        mongo_repository: MongoRepositoryInterface = Depends(
            Provide("mongo_repository")
        ),
    ):
        self._mongo_repository = mongo_repository

    async def count_completed_tasks_by_user(self, project_id: int, user_id: int) -> int:
        count = await self._mongo_repository.count_completed_tasks_by_user(
            TOPICS.TASK_UPDATED.value, project_id, user_id
        )
        return count
