from fastapi import FastAPI
import uvicorn

from src.models.seed import seed_all



app = FastAPI(
    title="JobFinder",
    description="Web-service for find job",
    version="version 1.0.0"
)


@app.on_event("startup")
async def on_startup():
    await seed_all()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)