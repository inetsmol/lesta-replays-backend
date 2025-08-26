from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.api.v1.replays import router as replays_router
from app.db.init import init_tortoise

app = FastAPI(title="WoT Record (MVP · Tortoise+SQLite)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_tortoise(app)

app.include_router(replays_router, prefix="/api/v1")