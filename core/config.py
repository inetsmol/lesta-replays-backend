from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # .../backend
PROJECT_ROOT = BASE_DIR.parent                  # корень репо

# БД: на MVP SQLite, позже заменим на Postgres
DB_URL = os.getenv("DB_URL", f"sqlite://{BASE_DIR / 'wotrec.db'}")

# Директории
UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(PROJECT_ROOT / "uploads"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
