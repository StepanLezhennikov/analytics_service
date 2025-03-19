from abc import ABC, abstractmethod

from app.config import TOPICS
from app.core.dto.task import TaskStatusStrDTO


class AnalyticsRepositoryInterface(ABC):
    @abstractmethod
    async def filter(self, collection: TOPICS, **filters) -> list:
        pass

    @abstractmethod
    async def get_tasks_statuses(
        self, collection: TOPICS, project_id: int, exclude_task_ids: list[int] = None
    ) -> list[TaskStatusStrDTO]:
        pass

    @abstractmethod
    async def count_completed_tasks_by_user(
        self, collection: TOPICS, project_id: int, user_id: int
    ) -> int:
        pass

    @abstractmethod
    async def get_avg_time_to_complete(
        self, collection: TOPICS, project_id: int
    ) -> int:
        pass
