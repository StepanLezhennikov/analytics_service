from typing import List

from fastapi import Depends
from dependency_injector.wiring import Provide

from app.config import TOPICS, TaskStatus
from app.core.dto.task import AvgTimeDTO, TaskStatusDTO
from app.core.interfaces.services.task import TaskServiceInterface
from app.core.interfaces.repositories.analytics_repo import AnalyticsRepositoryInterface


class TaskService(TaskServiceInterface):
    def __init__(
        self,
        analytics_repository: AnalyticsRepositoryInterface = Depends(
            Provide("analytics_repository")
        ),
    ):
        self._analytics_repository = analytics_repository

    async def get_tasks_statuses(self, project_id: int) -> List[TaskStatusDTO]:
        updated_tasks = await self._analytics_repository.get_tasks_statuses(
            TOPICS.TASK_UPDATED.value, project_id=project_id
        )
        updated_tasks_ids = [task.task_id for task in updated_tasks]
        tasks = await self._analytics_repository.get_tasks_statuses(
            TOPICS.TASK_CREATED.value,
            project_id=project_id,
            exclude_task_ids=updated_tasks_ids,
        )

        tasks = tasks + updated_tasks

        task_statuses = []
        for task in tasks:
            match task.status:
                case TaskStatus.BACKLOG:
                    task_statuses.append(TaskStatusDTO(task_id=task.task_id, status=0))
                case TaskStatus.RUNNING:
                    task_statuses.append(TaskStatusDTO(task_id=task.task_id, status=50))
                case TaskStatus.DONE:
                    task_statuses.append(
                        TaskStatusDTO(task_id=task.task_id, status=100)
                    )

        return task_statuses

    async def get_avg_time_to_complete(self, project_id: int) -> AvgTimeDTO:
        all_seconds = await self._analytics_repository.get_avg_time_to_complete(
            TOPICS.TASK_UPDATED.value, project_id
        )

        days, remainder = divmod(all_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        human_readable = f"{days}d {hours}h {minutes}m {seconds}s"
        return AvgTimeDTO(seconds=all_seconds, human_readable=human_readable)
