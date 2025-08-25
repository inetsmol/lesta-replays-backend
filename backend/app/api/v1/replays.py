from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from tortoise.expressions import Q

from backend.app.schemas.replay import ReplayOut
from backend.app.utils.storage import save_upload_async
from backend.app.parsers.replay_ingest import parse_replay
from backend.app.services.wn8 import wn8_single_battle_stub

from backend.app.models.replay import Replay

router = APIRouter(prefix="/replays", tags=["replays"])


@router.post("/upload", response_model=ReplayOut)
async def upload_replay(file: UploadFile = File(...), private: bool = Form(False)):
    # принимаем и .wotreplay, и .mtreplay
    if not (file.filename.endswith(".wotreplay") or file.filename.endswith(".mtreplay")):
        raise HTTPException(400, "Требуется файл с расширением .wotreplay или .mtreplay")

    sha1, path, size = await save_upload_async(file, file.filename)

    # дубликаты по SHA1
    exists = await Replay.get_or_none(file_sha1=sha1)
    if exists:
        return await ReplayOut.from_tortoise_orm(exists)

    parsed = await parse_replay(path)
    wn8 = wn8_single_battle_stub(
        result=parsed["result"],
        damage=parsed["damage"],
        frags=parsed["frags"],
        spotted=parsed["spotted"],
        defense=parsed["defense_points"],
    )

    r = await Replay.create(
        file_sha1=sha1, file_path=path, file_size=size,
        client_version=parsed["client_version"], region=parsed["region"], server=parsed["server"],
        map_name=parsed["map_name"], battle_type=parsed["battle_type"], battle_time=parsed["battle_time"],
        player_name=parsed["player_name"], vehicle=parsed["vehicle"], vehicle_tier=parsed["vehicle_tier"],
        result=parsed["result"], damage=parsed["damage"], frags=parsed["frags"], spotted=parsed["spotted"],
        defense_points=parsed["defense_points"], blocked=parsed["blocked"],
        credits=parsed["credits"], xp=parsed["xp"], bonds=parsed["bonds"], wn8=wn8,
        raw_common=parsed["raw_common"], raw_perf=parsed["raw_perf"], raw_econ=parsed["raw_econ"],
        private=private,
    )
    return await ReplayOut.from_tortoise_orm(r)


@router.get("", response_model=list[ReplayOut])
async def list_replays(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    public_only: bool = Query(True),
    search: str | None = Query(None, description="поиск по игроку/танку/карте"),
):
    q = Replay.filter()
    if public_only:
        q = q.filter(private=False)
    if search:
        q = q.filter(
            Q(player_name__icontains=search)
            | Q(vehicle__icontains=search)
            | Q(map_name__icontains=search)
        )
    rows = await q.order_by("-created_at").limit(limit).offset(offset)
    return [await ReplayOut.from_tortoise_orm(x) for x in rows]


@router.get("/{rid}", response_model=ReplayOut)
async def get_replay(rid: str):
    r = await Replay.get_or_none(id=rid)
    if not r:
        raise HTTPException(404, "Не найдено")
    return await ReplayOut.from_tortoise_orm(r)