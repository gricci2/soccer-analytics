import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

passes_df = pd.read_csv("../../data/processed/pass_locations_all.csv")

passes_df = passes_df.dropna(subset=['x', 'y'])

teams = passes_df['team_name'].unique()

#plt.figure(figsize=(12, 8))
pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

for team in teams:
    subset = passes_df[passes_df['team_name']== team]
    #pitch.kdeplot(subset['x'], subset['y'], ax=ax, cmap='Reds', fill=True) #heatmap
    pitch.scatter(subset['x'], subset['y'], ax=ax, alpha=0.5, label=team, s=100)
    #plt.scatter(subset['x'], subset['y'], alpha=0.5, label=team)

#plt.xlabel("Pitch X Coordinate")
#plt.ylabel("Pitch Y Coordinate")

plt.title("Pass Starting Locations by Team (mplsoccer)")
plt.legend()

plt.show()