import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

shots_df = pd.read_csv("../../data/processed/shot_map.csv")

#shots_df = shots_df.dropna(subset=['x', 'y', 'shot_statsbomb_xg'])

shots_df = shots_df.dropna(subset=['x', 'y'])

#shots_df = shots_df.sample(n=200000, random_state=42)

# teams = shots_df['team_name'].unique()

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

# for team in teams:
#     subset = shots_df[shots_df['team_name'] == team]
    
#     pitch.scatter(
#         subset['x'],
#         subset['y'],
#         ax=ax,
#         s=subset['shot_statsbomb_xg'] * 1000,
#         alpha=0.7,
#         label=team
#     )

# plt.legend()
#plt.title("Shot Map - Size = xG (mplsoccer)")
#plt.legend()

sns.kdeplot(
    x=shots_df['x'],
    y=shots_df['y'],
    fill=True,
    cmap='Reds',
    alpha=0.6,
    thresh=0.05,
    ax=ax
)


plt.title("Shot Heatmap (All Teams)")
plt.show()