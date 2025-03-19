from httpx import AsyncClient


async def test_count_tasks(http_client: AsyncClient, create_tasks):
    for i in range(3):
        await create_tasks(1)
    response = await http_client.get("/v1/projects/1/tasks/")

    assert response.status_code == 200

    assert response.json() == 3


async def test_count_tasks_with_deleted(
    http_client: AsyncClient, create_tasks, delete_task
):
    for i in range(3):
        await create_tasks(1)
    await delete_task(1)
    response = await http_client.get("/v1/projects/1/tasks/")

    assert response.status_code == 200

    assert response.json() == 2
