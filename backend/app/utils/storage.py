from __future__ import annotations

import hashlib
import os
from pathlib import Path

import aiofiles

from backend.app.core.config import UPLOAD_DIR

UPLOADS_PATH = Path(UPLOAD_DIR)
UPLOADS_PATH.mkdir(exist_ok=True, parents=True)

async def save_upload_async(upload_file, filename: str) -> tuple[str, str, int]:
    tmp_path = UPLOADS_PATH / (filename + ".part")
    sha1 = hashlib.sha1()
    size = 0

    async with aiofiles.open(tmp_path, "wb") as out:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            await out.write(chunk)
            sha1.update(chunk)
            size += len(chunk)

    digest = sha1.hexdigest()
    final_path = UPLOADS_PATH / f"{digest}.wotreplay"
    os.replace(tmp_path, final_path)
    return digest, str(final_path), size