import json
import pandas as pd
import pyodbc
import numpy as np

def load_event(file_path):
    with open(f"../data/raw/events/{file_path}", encoding="utf-8") as f:
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

    rows = list(events.itertuples(index=False, name=None))
    return rows