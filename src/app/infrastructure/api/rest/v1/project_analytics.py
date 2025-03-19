from fastapi import Depends, APIRouter
from dependency_injector.wiring import Provide, inject

from app.core.dto.task import AvgTimeDTO, TaskStatusDTO
from app.core.interfaces.services.task import TaskServiceInterface
from app.core.interfaces.services.user import UserServiceInterface
from app.core.interfaces.services.project import ProjectServiceInterface

router = APIRouter()


@router.get("/amount/")
@inject
async def count_projects(
    project_service: ProjectServiceInterface = Depends(Provide("project_service")),
) -> int:
    return await project_service.count_projects()


@router.get("/{project_id}/tasks/")
@inject
async def count_project_tasks(
    project_id: int,
    project_service: ProjectServiceInterface = Depends(Provide("project_service")),
) -> int:
    return await project_service.count_tasks_in_project(project_id)


@router.get("/{project_id}/users/")
@inject
async def count_project_users(
    project_id: int,
    project_service: ProjectServiceInterface = Depends(Provide("project_service")),
):
    return await project_service.count_users_in_project(project_id)


@router.get("/{project_id}/statuses/")
@inject
async def get_task_statuses(
    project_id: int,
    task_service: TaskServiceInterface = Depends(Provide("task_service")),
) -> list[TaskStatusDTO]:
    return await task_service.get_tasks_statuses(project_id)


@router.get("/{project_id}/users/{user_id}/completed_tasks/")
@inject
async def count_completed_tasks_by_user(
    project_id: int,
    user_id: int,
    user_service: UserServiceInterface = Depends(Provide("user_service")),
) -> int:
    return await user_service.count_completed_tasks_by_user(project_id, user_id)


@router.get("/{project_id}/average_time/")
@inject
async def count_average_time_to_complete(
    project_id: int,
    task_service: TaskServiceInterface = Depends(Provide("task_service")),
) -> AvgTimeDTO:
    return await task_service.get_avg_time_to_complete(project_id)
