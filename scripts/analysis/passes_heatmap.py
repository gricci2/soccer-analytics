import pandas as pd
import pyodbc
from mplsoccer import Pitch

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(localdb)\\MSSQLLocalDB;"
    "DATABASE=SoccerAnalytics;"
    "Trusted_Connection=yes;"
)

query = open("../../sql/pass_locations_all.sql").read()
all_passes_df = pd.read_sql(query, conn)

all_passes_df = all_passes_df.sample(n=50000, random_state=42)

pitch = Pitch(pitch_type='statsbomb')

bin_stat = pitch.bin_statistic(
    all_passes_df['x'],
    all_passes_df['y'],
    statistic='count',
    bins=(25, 25)
)

heatmap_df = pd.DataFrame(bin_stat['statistic'])

heatmap_df = heatmap_df.stack().reset_index()
heatmap_df.columns = ['y_bin', 'x_bin', 'count']

heatmap_df.to_csv('../../data/processed/pass_heatmap.csv', index=False)

print("Saved pass_heatmap.csv")