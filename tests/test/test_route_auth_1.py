import pytest
from fastapi import HTTPException, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes.users import router
from src.services.auth import Auth
from src.services.roles import RoleChecker

# Можливо, потрібно буде імпортувати функції та моделі для створення користувачів і ролей для тестів

# Фіктивні дані для тестування
fake_user_data = {
    "email": "test@example.com",
    "password": "testpassword",
    "username": "testuser",
}


# Тестова функція для створення користувача
async def create_test_user(session: AsyncSession):
    # Створити користувача у тестовій базі даних
    ...


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=router) as client:
        # Спроба створення користувача з коректними даними
        response = await client.post("/api/users/", json=fake_user_data)
        assert response.status_code == status.HTTP_201_CREATED

        # Спроба створення користувача з некоректними даними
        invalid_user_data = fake_user_data.copy()
        invalid_user_data.pop("email")  # Видалити email
        response = await client.post("/api/users/", json=invalid_user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Тестування авторизації
@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=router) as client:
        # Спроба входу з коректними даними
        response = await client.post("/api/users/login/", data=fake_user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

        # Спроба входу з некоректними даними
        invalid_user_data = fake_user_data.copy()
        invalid_user_data["password"] = "wrongpassword"
        response = await client.post("/api/users/login/", data=invalid_user_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тестування отримання інформації про користувача
@pytest.mark.asyncio
async def test_get_user_info():
    async with AsyncClient(app=router) as client:
        # Створення тестового користувача перед запитом
        async with AsyncSession() as session:
            await create_test_user(session)

        # Спроба отримати інформацію про користувача з авторизаційним токеном
        access_token = Auth().create_access_token({"sub": fake_user_data["email"]})
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/users/me/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == fake_user_data["email"]

        # Спроба отримати інформацію про користувача без авторизаційного токену
        response = await client.get("/api/users/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тестування ролей доступу
@pytest.mark.asyncio
async def test_access_roles():
    async with AsyncClient(app=router) as client:
        # Створення тестового користувача перед запитом
        async with AsyncSession() as session:
            await create_test_user(session)

        # Спроба виконати дію, яка доступна тільки адміністраторам
        access_token = Auth().create_access_token({"sub": fake_user_data["email"]})
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/users/admin/", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Спроба виконати дію, яка доступна звичайним користувачам
        response = await client.get("/api/users/user/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
