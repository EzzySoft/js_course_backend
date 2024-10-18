import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.trips import router


# Создание тестового приложения
@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

# Фикстура для клиента
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

# Фикстура для создания сессии
@pytest.fixture
async def db_session() -> AsyncSession:
    # Логика создания тестовой сессии базы данных
    pass

@pytest.mark.asyncio
async def test_create_trip(client: AsyncClient, db_session: AsyncSession):
    trip_data = {
        "field1": "value1",  # Заполните в соответствии с вашей схемой
        "field2": "value2"
    }
    response = await client.post("/", json=trip_data, cookies={"session_id": "test_session_id"})
    assert response.status_code == 200
    assert response.json() == {"success": True}  # Убедитесь, что ожидаете правильный ответ

@pytest.mark.asyncio
async def test_get_trip(client: AsyncClient, db_session: AsyncSession):
    trip_id = 1  # Замените на существующий trip_id
    response = await client.get(f"/{trip_id}")
    assert response.status_code == 200
    assert "field1" in response.json()  # Проверьте, что данные возвращаются корректно

@pytest.mark.asyncio
async def test_delete_trip(client: AsyncClient, db_session: AsyncSession):
    trip_id = 1  # Замените на существующий trip_id
    response = await client.delete(f"/{trip_id}", cookies={"session_id": "test_session_id"})
    assert response.status_code == 200
    assert response.json() == {"success": True}  # Убедитесь, что ожидаете правильный ответ

@pytest.mark.asyncio
async def test_get_user_trips(client: AsyncClient, db_session: AsyncSession):
    response = await client.get("/get_user_trips/", cookies={"session_id": "test_session_id"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Проверьте, что возвращается список поездок
