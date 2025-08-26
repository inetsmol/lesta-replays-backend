from __future__ import annotations

import os, time, jwt
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import CORS_ORIGINS
from api.v1.replays import router as replays_router
from db.init import init_tortoise

load_dotenv()

app = FastAPI(title="WoT Record (MVP · Tortoise+SQLite)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_tortoise(app)

app.include_router(replays_router, prefix="/api/v1")