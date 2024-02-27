from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from main import app
from src.database.models import Base
from src.database.models import Comment


# Функція для створення тестової бази даних з використанням Faker
def create_test_db():
    engine = create_engine("sqlite:///./test.db")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    faker = Faker()

    # Створення тестових даних у базі даних
    for _ in range(10):
        text = faker.text()
        comment = Comment(text=text)
        db.add(comment)
    db.commit()
    db.close()


# Перевизначення методу отримання з'єднання з базою даних у додатку
def override_get_db():
    engine = create_engine("sqlite:///./test.db")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Перевірка невірного введення даних для маршруту create_comment
def test_invalid_create_comment():
    client = TestClient(app)
    response = client.post("/comments/create_comment/1", json={})
    assert response.status_code == 422  # Очікується код помилки про неприпустимий запит


# Перевірка невірного введення даних для маршруту edit_comment
def test_invalid_edit_comment():
    client = TestClient(app)
    response = client.put("/comments/edit/1", json={})
    assert response.status_code == 422  # Очікується код помилки про неприпустимий запит


# Перевірка невірного введення даних для маршруту delete_comment
def test_invalid_delete_comment():
    client = TestClient(app)
    response = client.delete("/comments/delete/9999")  # Неправильний ID коментаря
    assert response.status_code == 404  # Очікується код помилки про неправильний запит


# Перевірка невірного введення даних для маршруту get_comment_photo_id_route
def test_invalid_get_comment_photo_id_route():
    client = TestClient(app)
    response = client.get("/comments/get_comment_photo_id/9999")  # Неправильний ID фото
    assert response.status_code == 404  # Очікується код помилки про неправильний запит


# Перевірка невірного введення даних для маршруту get_comment_photo_user_id_route
def test_invalid_get_comment_photo_user_id_route():
    client = TestClient(app)
    response = client.get("/comments/get_comment_id/")  # Відсутній user_id
    assert response.status_code == 404  # Очікується код помилки про неправильний запит


# Запуск тесту
if __name__ == "__main__":
    create_test_db()
    test_invalid_create_comment()
    test_invalid_edit_comment()
    test_invalid_delete_comment()
    test_invalid_get_comment_photo_id_route()
    test_invalid_get_comment_photo_user_id_route()
