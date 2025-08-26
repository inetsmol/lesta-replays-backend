from __future__ import annotations
from tortoise import fields, models

class Replay(models.Model):
    class Meta:
        table = "replays"
        indexes = ("file_sha1", "player_name", "vehicle", "map_name",
                   "client_version", "region", "private")

    id = fields.UUIDField(pk=True)
    file_sha1 = fields.CharField(max_length=40, unique=True, index=True)
    file_path = fields.CharField(max_length=512)
    file_size = fields.IntField()

    client_version = fields.CharField(max_length=32, index=True)
    region = fields.CharField(max_length=8, index=True)         # EU/NA/RU/ASIA
    server = fields.CharField(max_length=32, null=True)
    map_name = fields.CharField(max_length=64, index=True)
    battle_type = fields.CharField(max_length=32, index=True)
    battle_time = fields.DatetimeField()

    player_name = fields.CharField(max_length=64, index=True)
    vehicle = fields.CharField(max_length=64, index=True)
    vehicle_tier = fields.IntField()

    result = fields.CharField(max_length=16)                     # Victory/Defeat/Draw/Unknown
    damage = fields.IntField()
    frags = fields.IntField()
    spotted = fields.IntField()
    defense_points = fields.IntField()
    blocked = fields.IntField()
    credits = fields.IntField()
    xp = fields.IntField()
    bonds = fields.IntField(default=0)

    wn8 = fields.FloatField()

    raw_common = fields.JSONField()
    raw_perf = fields.JSONField()
    raw_econ = fields.JSONField()

    private = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)