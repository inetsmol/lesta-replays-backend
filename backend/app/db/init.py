from __future__ import annotations

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from backend.app.core.config import DB_URL


def init_tortoise(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["backend.app.models.replay"]},
        generate_schemas=True,  # MVP: авто-создание таблиц. В проде → Aerich миграции.
        add_exception_handlers=True,
    )