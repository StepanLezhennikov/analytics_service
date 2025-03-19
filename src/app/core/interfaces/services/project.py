from abc import ABC, abstractmethod


class ProjectServiceInterface(ABC):
    @abstractmethod
    async def count_projects(self) -> int:
        pass

    @abstractmethod
    async def count_tasks_in_project(self, project_id: int) -> int:
        pass

    @abstractmethod
    async def count_users_in_project(self, project_id: int) -> int:
        pass
