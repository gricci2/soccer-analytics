import json
import pandas as pd
import pyodbc

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

#for _, row in events.iterrows()

print(events.head(20))
print(events.info())
print(events.columns.to_list())


#cursor.execute("SELECT DB_NAME()")
#print(cursor.fetchone())
#for col in df.columns:
#    print(col)