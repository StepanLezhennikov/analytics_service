from httpx import AsyncClient


async def test_count_completed_tasks(http_client: AsyncClient, finish_task):
    await finish_task(task_id=1, project_id=1, user_id=1)
    await finish_task(task_id=2, project_id=1, user_id=1)
    response = await http_client.get("/v1/projects/1/users/1/completed_tasks/")
    assert response.status_code == 200
    assert response.json() == 2


async def test_count_completed_tasks_with_deleted(
    http_client: AsyncClient, finish_task, delete_task
):
    await finish_task(task_id=1, project_id=1, user_id=1)
    await finish_task(task_id=2, project_id=1, user_id=1)
    await delete_task(1)
    response = await http_client.get("/v1/projects/1/users/1/completed_tasks/")
    assert response.status_code == 200
    assert response.json() == 1
