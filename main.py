# main.py
import uvicorn
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from src.database.db import get_async_db
from src.routes import auth, users, photos, comments, transforms

#import aioredis
import redis.asyncio as redis_

#async def get_redis_conn():
#    return await aioredis.create_redis_pool('redis://localhost')

app = FastAPI()

@app.on_event("startup")
#async def startup():
#    redis_conn = await get_redis_conn()
#    await FastAPILimiter.init(redis_conn)
async def startup():
    r = await redis_.Redis(
        host="localhost",
        port=6379,
        db=0,        
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello world!"}

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(transforms.router, prefix="/api")
app.include_router(comments.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8001)
