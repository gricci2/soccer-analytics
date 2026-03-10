import json
import pandas as pd

file_path = "../data/raw/events/15946.json"

with open(file_path, encoding="utf-8") as f:
    data = json.load(f)

print(f"Total events loaded:  {len(data)}")

df = pd.json_normalize(data)

# all_columns = list(df.columns)
# print(df.columns.to_list())
players = df["player.name"]
unique_players = set(players)
for player in unique_players:
    print(player)