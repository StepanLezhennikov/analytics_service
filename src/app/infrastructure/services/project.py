from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS
from app.core.interfaces.services.project import ProjectServiceInterface
from app.core.interfaces.repositories.analytics_repo import AnalyticsRepositoryInterface


class ProjectService(ProjectServiceInterface):
    def __init__(
        self,
        analytics_repository: AnalyticsRepositoryInterface = Depends(
            Provide("analytics_repository")
        ),
    ):
        self._analytics_repository = analytics_repository

    async def count_projects(self) -> int:
        created_projects_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.PROJECT_CREATED.value
            )
        )
        deleted_projects_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.PROJECT_DELETED.value
            )
        )

        return created_projects_amount - deleted_projects_amount

    async def count_tasks_in_project(self, project_id: int) -> int:
        tasks_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.TASK_CREATED.value, project_id=project_id
            )
        )
        deleted_tasks_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.TASK_DELETED.value, project_id=project_id
            )
        )
        return tasks_amount - deleted_tasks_amount

    async def count_users_in_project(self, project_id: int) -> int:
        users_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.USER_CREATED.value, project_id=project_id
            )
        )
        deleted_users_amount = len(
            await self._analytics_repository.filter(
                collection=TOPICS.USER_DELETED.value, project_id=project_id
            )
        )
        return users_amount - deleted_users_amount
