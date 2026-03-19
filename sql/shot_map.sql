SELECT
    player_name,
    team_name,
    x,
    y,
    shot_statsbomb_xg
FROM Events
WHERE type_name = 'Shot'
    AND x IS NOT NULL
    AND y IS NOT NULL;