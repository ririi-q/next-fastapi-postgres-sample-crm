from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import Config as AppConfig
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NextFastApp",
    description="NextFastApp API description"
)

# セッションミドルウェアを追加
app.add_middleware(SessionMiddleware, secret_key=AppConfig.SECRET_KEY)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

v1_app = FastAPI(
    title="NextFastApp API v1",
    description="Version 1 of the NextFastApp",
    openapi_tags=[
        {"name": "users", "description": "User operations"},
        {"name": "companies", "description": "Company operations"},
    ]
)
v1_app.include_router(v1_router)

app.mount("/api/v1", v1_app)

# health check
@app.get("/health")
async def health():
    return {"status": "ok"}
