import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

shots_df = pd.read_csv("../../data/processed/shot_map.csv")

shots_df = shots_df.dropna(subset=['x', 'y', 'shot_statsbomb_xg'])

teams = shots_df['team_name'].unique()

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

for team in teams:
    subset = shots_df[shots_df['team_name'] == team]
    
    pitch.scatter(
        subset['x'],
        subset['y'],
        ax=ax,
        s=subset['shot_statsbomb_xg'] * 1000,
        alpha=0.7,
        label=team
    )

plt.legend()
plt.title("Shot Map - Size = xG (mplsoccer)")
plt.legend()

plt.show()