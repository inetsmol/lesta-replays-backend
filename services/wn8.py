from __future__ import annotations

def wn8_single_battle_stub(result: str, damage: int, frags: int, spotted: int, defense: int) -> float:
    base = damage * 0.001 + frags * 120 + spotted * 40 + defense * 15
    if result == "Victory":
        base *= 1.1
    elif result == "Defeat":
        base *= 0.9
    return round(base, 2)