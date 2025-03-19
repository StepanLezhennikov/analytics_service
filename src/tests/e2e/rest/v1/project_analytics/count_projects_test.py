from httpx import AsyncClient


async def test_count_projects(http_client: AsyncClient, create_projects):
    projects = await create_projects(3)
    response = await http_client.get("/v1/projects/amount/")

    assert response.status_code == 200

    assert response.json() == len(projects)


async def test_count_projects_with_deleted(
    http_client: AsyncClient, create_projects, delete_project
):
    projects = await create_projects(3)
    await delete_project(1)
    response = await http_client.get("/v1/projects/amount/")

    assert response.status_code == 200

    assert response.json() == len(projects) - 1
