import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

passes_df = pd.read_csv("../../data/processed/pass_locations_all.csv")

passes_df = passes_df.dropna(subset=['x', 'y'])

passes_df = passes_df.sample(n=50000, random_state=42)

#team looping removed for heatmap
#teams = passes_df['team_name'].unique()

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

# for team in teams:
#     subset = passes_df[passes_df['team_name']== team]
#     pitch.scatter(subset['x'], subset['y'], ax=ax, alpha=0.5, label=team, s=100)

# bin_stat = pitch.bin_statistic(
#     passes_df['x'],
#     passes_df['y'],
#     statistic='count',
#     bins=(25, 25)
# )

# pitch.heatmap(bin_stat, ax=ax, cmap='Reds')

sns.kdeplot(
    x=passes_df['x'],
    y=passes_df['y'],
    fill=True,
    cmap='Reds',
    alpha=0.6,
    thresh=0.05,
    ax=ax
)



#plt.title("Pass Starting Locations by Team (mplsoccer)")
#plt.legend()
plt.title("Pass Heatmap (All Teams)")
plt.show()