from httpx import AsyncClient


async def test_count_users(http_client: AsyncClient, create_users):
    for i in range(3):
        await create_users(1)
    response = await http_client.get("/v1/projects/1/users/")

    assert response.status_code == 200

    assert response.json() == 3


async def test_count_users_with_deleted(
    http_client: AsyncClient, create_users, delete_user
):
    for i in range(3):
        await create_users(1)
    await delete_user(1)
    response = await http_client.get("/v1/projects/1/users/")

    assert response.status_code == 200

    assert response.json() == 2
