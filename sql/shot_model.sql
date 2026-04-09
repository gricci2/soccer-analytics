SELECT
    x,
    y,
    shot_statsbomb_xg,
    CASE 
        WHEN shot_outcome_name = 'Goal' THEN 1
        ELSE 0
    END AS goal
FROM Events
WHERE type_name = 'Shot'
AND x IS NOT NULL
AND y IS NOT NULL;