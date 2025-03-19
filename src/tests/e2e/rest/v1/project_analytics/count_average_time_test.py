import datetime

from httpx import AsyncClient


async def test_count_average_time_to_complete(http_client: AsyncClient, finish_task):
    await finish_task(task_id=1, project_id=1, user_id=1)
    await finish_task(task_id=2, project_id=1, user_id=1)
    response = await http_client.get("/v1/projects/1/average_time/")
    assert response.status_code == 200
    assert (
        response.json()["seconds"]
        == (datetime.timedelta(days=2) - datetime.timedelta(days=1) / 2).total_seconds()
    )


async def test_count_average_time_to_complete_with_deleted(
    http_client: AsyncClient, finish_task, delete_task
):
    await finish_task(task_id=1, project_id=1, user_id=1)
    await finish_task(task_id=2, project_id=1, user_id=1)
    await delete_task(1)
    response = await http_client.get("/v1/projects/1/average_time/")
    assert response.status_code == 200
    assert response.json()["seconds"] == datetime.timedelta(days=2).total_seconds()
