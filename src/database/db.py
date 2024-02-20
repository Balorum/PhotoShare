from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

print("*"*120)
print(SQLALCHEMY_DATABASE_URL)
print("*"*120)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_async_db():
    async_db = async_session()
    try:
        yield async_db
    finally:
        await async_db.close()


get_db = get_async_db