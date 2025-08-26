from __future__ import annotations
from datetime import datetime, date
from wotreplay import ReplayData
import asyncio
import base64


def _get_from(obj, key, default=None):
    """
    Безопасно достает значение по ключу из dict ИЛИ из list[dict].
    Берем первое попавшееся значение из списка словарей.
    """
    if isinstance(obj, dict):
        return obj.get(key, default)
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and key in item:
                return item[key]
    return default


def _int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default


def _str(v, default=""):
    try:
        if v is None:
            return default
        return str(v)
    except Exception:
        return default


def _to_jsonable(obj):
    """
    Рекурсивно приводит объект к JSON-совместимому виду:
    - datetime/date -> ISO8601 строка
    - bytes/bytearray -> base64 строка
    - tuple -> list
    - остальные нестандартные типы -> str(...)
    """
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, (bytes, bytearray)):
        return base64.b64encode(obj).decode("ascii")
    if isinstance(obj, dict):
        return {str(k): _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    # fallback для всего прочего (Decimal, custom, и т.п.)
    return str(obj)


def _parse_sync(file_path: str) -> dict:
    r = ReplayData(file_path=file_path, db_path="", db_name="", load=False)
    print(r.common)
    # Блоки могут быть dict ИЛИ list[dict] — не полагаемся на .get()
    perf = r.battle_performance or {}
    econ = r.battle_economy or {}
    meta = r.battle_metadata or {}
    common = r.common or {}

    # ---------- Результат боя ----------
    result = "Unknown"
    winner_team = _get_from(perf, "winnerTeam")
    # playerTeam может быть либо в meta, либо в common
    player_team = _get_from(meta, "playerTeam")
    if player_team is None:
        player_team = _get_from(common, "playerTeam")

    if winner_team is not None and player_team is not None:
        result = "Victory" if winner_team == player_team else "Defeat"
    elif winner_team == 0:
        result = "Draw"

    # ---------- Метаданные ----------
    client_version = _str(_get_from(common, "clientVersionFromXml") or _get_from(common, "clientVersion") or "")
    region = _str(_get_from(common, "region") or _get_from(meta, "region") or "EU")
    server = _str(_get_from(common, "serverName"), default=None)

    map_name = _str(_get_from(meta, "mapDisplayName") or _get_from(meta, "mapName") or "")
    battle_type = _str(_get_from(meta, "gameplayID") or _get_from(meta, "battleType") or "Standard Battle")

    dt_ms = _get_from(common, "dateTime")
    if isinstance(dt_ms, (int, float)):
        battle_time = datetime.fromtimestamp(dt_ms / 1000.0)
    else:
        battle_time = datetime.utcnow()

    player_name = _str(_get_from(common, "playerName") or _get_from(meta, "playerName") or "")
    vehicle = _str(_get_from(meta, "playerVehicle") or _get_from(common, "vehicleName") or "")
    vehicle_tier = _int(_get_from(meta, "playerVehicleLevel") or _get_from(common, "vehicleLevel") or 0)

    # ---------- Перфоманс ----------
    damage = _int(_get_from(perf, "damageDealt"))
    frags = _int(_get_from(perf, "kills"))
    spotted = _int(_get_from(perf, "spotted"))
    defense_points = _int(_get_from(perf, "droppedCapturePoints"))
    blocked = _int(_get_from(perf, "damageBlockedByArmor"))

    # ---------- Экономика ----------
    credits = _int(_get_from(econ, "credits", default=0))
    xp = _int(_get_from(econ, "xp", default=0))
    bonds = _int(_get_from(econ, "crystal", default=0))

    # ---------- Сырые блоки (JSON-совместимые) ----------
    raw_common_json = _to_jsonable(common)
    raw_perf_json = _to_jsonable(perf)
    raw_econ_json = _to_jsonable(econ)

    return {
        "client_version": client_version,
        "region": region,
        "server": server,
        "map_name": map_name,
        "battle_type": battle_type,
        "battle_time": battle_time,
        "player_name": player_name,
        "vehicle": vehicle,
        "vehicle_tier": vehicle_tier,
        "result": result,
        "damage": damage,
        "frags": frags,
        "spotted": spotted,
        "defense_points": defense_points,
        "blocked": blocked,
        "credits": credits,
        "xp": xp,
        "bonds": bonds,
        "raw_common": raw_common_json,
        "raw_perf": raw_perf_json,
        "raw_econ": raw_econ_json,
    }


async def parse_replay(file_path: str) -> dict:
    # wotreplay синхронный → гоняем в thread pool
    return await asyncio.to_thread(_parse_sync, file_path)
