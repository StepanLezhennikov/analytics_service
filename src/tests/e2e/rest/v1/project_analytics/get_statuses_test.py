from httpx import AsyncClient


async def test_statuses(http_client: AsyncClient, create_tasks):
    await create_tasks(1)
    response = await http_client.get("/v1/projects/1/statuses/")
    assert response.status_code == 200
    task_statuses = response.json()
    assert len(task_statuses) == 1
    assert task_statuses[0]["task_id"] == 1
    assert task_statuses[0]["status"] == 0


async def test_statuses_with_deleted(
    http_client: AsyncClient, create_tasks, delete_task
):
    await create_tasks(2)
    await delete_task(2)
    response = await http_client.get("/v1/projects/2/statuses/")
    assert response.status_code == 200
    task_statuses = response.json()
    assert len(task_statuses) == 0
