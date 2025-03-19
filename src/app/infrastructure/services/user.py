from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS
from app.core.interfaces.services.user import UserServiceInterface
from app.core.interfaces.repositories.analytics_repo import AnalyticsRepositoryInterface


class UserService(UserServiceInterface):
    def __init__(
        self,
        analytics_repository: AnalyticsRepositoryInterface = Depends(
            Provide("analytics_repository")
        ),
    ):
        self._analytics_repository = analytics_repository

    async def count_completed_tasks_by_user(self, project_id: int, user_id: int) -> int:
        count = await self._analytics_repository.count_completed_tasks_by_user(
            TOPICS.TASK_UPDATED.value, project_id, user_id
        )
        return count
