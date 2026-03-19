SELECT team_name, x, y
FROM Events
WHERE type_name = 'Pass'
	AND x IS NOT NULL
	AND y IS NOT NULL
ORDER BY team_name;