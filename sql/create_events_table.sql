USE SoccerAnalytics;
GO

IF NOT EXISTS (
    SELECT *
    FROM sys.tables
    WHERE name = 'Events'
)
BEGIN
    CREATE TABLE Events (
        id NVARCHAR(50),
        event_index INT,
        period INT,
        timestamp NVARCHAR(20),
        minute INT,
        second INT,
        possession INT,
        team_name NVARCHAR(100),
        player_name NVARCHAR(100),
        type_name NVARCHAR(50),
        pass_recipient_name NVARCHAR(100),
        pass_length FLOAT,
        shot_statsbomb_xg FLOAT,
        x FLOAT,
        y FLOAT
    );
END