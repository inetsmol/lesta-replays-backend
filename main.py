from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.v1.replays import router as replays_router
from api.v1.auth import router as auth_router
from core.config import CORS_ORIGINS
from db.init import init_tortoise

load_dotenv()

app = FastAPI(title="WoT Record (MVP · Tortoise+SQLite)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.environ["APP_SECRET_KEY"])

init_tortoise(app)

app.include_router(replays_router,  prefix="/api/v1")
app.include_router(auth_router,  prefix="/api/v1")