from fastapi import FastAPI
import uvicorn

from src.models.seed import seed_all
from src.redis.redis_client import RedisClient
from src.api.v1.router import api_router


app = FastAPI(
    title="JobFinder",
    description="Web-service for find job",
    version="version 1.0.0"
)
app.include_router(api_router)

@app.on_event("startup")
async def startup():
    await seed_all()
    redis_client = RedisClient()
    await redis_client.connect()
    app.state.redis_client = redis_client

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis_client.close()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)