from wotreplay import ReplayData
replay = ReplayData(file_path='20250825_1102_ussr-R1008_T34_85M_NewOnBoarding_108_normandy_nom.mtreplay',
                    db_path='', db_name='', load=False)

print(replay.battle_metadata)
print(replay.battle_performance)
print(replay.common)
print(replay.battle_frags)
print(replay.battle_economy)
print(replay.battle_xp)