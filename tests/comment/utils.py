from faker import Faker
from src.database.models import Comment, User
from datetime import datetime, timedelta
import random

fake = Faker()


def generate_user() -> User:
    return User(
        username=fake.user_name(),
        email=fake.email(),
        full_name=fake.name(),
        hashed_password=fake.password(),
        is_active=True,
        is_superuser=False,
    )


def generate_comment(user_id: int, photo_id: int) -> Comment:
    return Comment(
        text=fake.paragraph(),
        user_id=user_id,
        photo_id=photo_id,
        created_at=datetime.now() - timedelta(days=random.randint(1, 10)),
        updated_at=datetime.now(),
        update_status=False,
    )
