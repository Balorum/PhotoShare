import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi_limiter import FastAPILimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import photos, tags, auth, users, comments, transforms, ratings
from src.conf.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    # r = await redis.Redis(
    #     host=settings.redis_host,
    #     port=settings.redis_port,
    #     password=settings.redis_password,
    #     db=0,
    #     encoding="utf-8",
    #     decode_responses=True
    # )
    # await FastAPILimiter.init(r)
    pass


@app.get("/")
def read_root():
    return {"message": "Hello world!"}


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(transforms.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(ratings.router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000)
