from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from api import router_api_v1
from config import settings
from models import database_helper

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database_helper.dispose()


main_app = FastAPI(
    title="Kuda Service API",
    description="N/A",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    middleware=[Middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3001", "http://localhost:3000", "http://localhost", "http://localhost:8099",],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )],
    lifespan=lifespan
)

main_app.include_router(router_api_v1, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )

