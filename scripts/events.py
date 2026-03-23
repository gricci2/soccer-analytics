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

file_path = "../data/raw/events/15956.json"

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

obj_cols = ['player_name', 'pass_recipient_name']

for col in obj_cols:
    events[col] = events[col].apply(lambda x: x.strip() if isinstance(x, str) and x.strip() != "" else None)

    events[col] = events[col].replace({np.nan: None})

print(events.iloc[0]['player_name'])
print(type(events.iloc[0]['player_name']))

print("Check types after cleaning:")
print(events.dtypes)
print(events[float_cols + obj_cols].head())

rows = list(events.itertuples(index=False, name=None))

cursor.fast_executemany = True
cursor.executemany("""
    INSERT INTO Events (
        id, event_index, period, timestamp, minute, second,
        possession, team_name, player_name, type_name,
        pass_recipient_name, pass_length, shot_statsbomb_xg, x, y
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

conn.commit()

cursor.execute("SELECT COUNT(*) FROM Events")
print(cursor.fetchone()[0])

print(events.head(20))
print(events.info())
print(events.columns.to_list())
