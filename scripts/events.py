import json
import pandas as pd
import pyodbc
import numpy as np

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=SoccerAnalytics;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()



file_path = "../data/raw/events/15946.json"

with open(file_path, encoding="utf-8") as f:
    data = json.load(f)

print(f"Total events loaded:  {len(data)}")

df = pd.json_normalize(data)

columns = [
    "id",
    "index",
    "period",
    "timestamp",
    "minute",
    "second",
    "possession",
    "team.name",
    "player.name",
    "type.name",
    "location",
    "pass.recipient.name",
    "pass.length",
    "shot.statsbomb_xg"
]

events = df[columns].copy()

events["x"] = events["location"].apply(
    lambda loc: loc[0] if isinstance(loc, list) else None
    )

events["y"] = events["location"].apply(
    lambda loc: loc[1] if isinstance(loc, list) else None
    )

events = events.drop(columns=["location"])
events.columns = events.columns.str.replace(".", "_", regex=False)
events = events.rename(columns={"index": "event_index"})

float_cols = ['pass_length', 'shot_statsbomb_xg', 'x', 'y']

for col in float_cols:
    events[col] = events[col].apply(
        lambda x: float(x) if isinstance(x, (int, float)) and not np.isnan(x) and not np.isinf(x) else None
    )

    events[col] = events[col].replace({np.nan: None})


events[float_cols] = events[float_cols].where(pd.notnull(events[float_cols]), None)

obj_cols = ['player_name', 'pass_recipient_name']

for col in obj_cols:
    events[col] = events[col].apply(lambda x: x.strip() if isinstance(x, str) and x.strip() != "" else None)

    events[col] = events[col].replace({np.nan: None})

print(events.iloc[0]['player_name'])
print(type(events.iloc[0]['player_name']))

print("Check types after cleaning:")
print(events.dtypes)
print(events[float_cols + obj_cols].head())

for i, row in events.iterrows():
    try:
        cursor.execute("""
    INSERT INTO Events (
        id, event_index, period, timestamp, minute, second,
        possession, team_name, player_name, type_name,
        pass_recipient_name, pass_length, shot_statsbomb_xg, x, y
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""",
    row['id'],
    int(row['event_index']),
    int(row['period']),
    row['timestamp'],
    int(row['minute']),
    int(row['second']),
    int(row['possession']),
    row['team_name'],
    row['player_name'],
    row['type_name'],
    row['pass_recipient_name'],
    row['pass_length'],
    row['shot_statsbomb_xg'],
    row['x'],
    row['y']
)
    except Exception as e:
        print(f"❌ Error at row {i}")
        print(row[float_cols + ['player_name', 'pass_recipient_name']])
        raise e

conn.commit()

cursor.execute("SELECT COUNT(*) FROM Events")
print(cursor.fetchone()[0])

print(events.head(20))
print(events.info())
print(events.columns.to_list())
