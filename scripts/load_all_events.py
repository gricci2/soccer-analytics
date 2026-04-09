import os
import json
import pandas as pd
import pyodbc
import numpy as np
import math
from load_single_event import load_event

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=SoccerAnalytics;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
cursor.fast_executemany = True
TABLE = "Events"
data_dir = "../data/raw/events/"

insert_query = f"""
        INSERT INTO {TABLE} (
            id, event_index, period, timestamp, minute, second, possession, 
            team_name, player_name, type_name,
            pass_recipient_name, pass_length, shot_statsbomb_xg, shot_outcome_name, x, y
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

batch_size = 1000
all_rows = []
sqlTableTotal = 0
for match_file in os.listdir(data_dir):
    if not match_file.endswith(".json"):
        continue  # skip non-json files
    
    rows = load_event(match_file)

    all_rows.extend(rows)
    sqlTableTotal += len(rows)
    if len(all_rows) >= batch_size:
        cursor.executemany(insert_query, all_rows)
        all_rows = []
    
    #match_path = os.path.join(data_dir, match_file)

if all_rows:
    cursor.executemany(insert_query, all_rows)

print(f"Total rows inserted: {sqlTableTotal}")
conn.commit()