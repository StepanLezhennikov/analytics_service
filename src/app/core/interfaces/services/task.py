from abc import ABC, abstractmethod
from typing import List

from app.core.dto.task import AvgTimeDTO, TaskStatusDTO


class TaskServiceInterface(ABC):
    @abstractmethod
    async def get_tasks_statuses(self, project_id: int) -> List[TaskStatusDTO]:
        pass

    @abstractmethod
    async def get_avg_time_to_complete(self, project_id: int) -> AvgTimeDTO:
        pass
