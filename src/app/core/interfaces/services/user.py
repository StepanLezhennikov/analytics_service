from abc import ABC, abstractmethod


class UserServiceInterface(ABC):
    @abstractmethod
    async def count_completed_tasks_by_user(self, project_id: int, user_id: int) -> int:
        pass
