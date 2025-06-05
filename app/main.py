from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, todos
from app.core.config import settings
from app.utils.database import engine
from app.domain.models.base import BaseModel

# データベーステーブル作成
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(
    title="SAMPLE Todo API",
    description="Simple Todo API for SAMPLE Mobile App",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["認証"]
)
app.include_router(
    todos.router,
    prefix="/api/v1/todos",
    tags=["Todo管理"]
)


@app.get("/")
async def root():
    return {"message": "SAMPLE Todo API is running!", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
