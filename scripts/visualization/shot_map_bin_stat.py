import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

shots_df = pd.read_csv("../../data/processed/shot_map.csv")

shots_df = shots_df.dropna(subset=['x', 'y'])

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

bin_stat = pitch.bin_statistic(
    shots_df['x'],
    shots_df['y'],
    statistic='count',
    bins=(25, 25)
)

pcm = pitch.heatmap(bin_stat, ax=ax, cmap='Reds')

plt.colorbar(pcm, ax=ax)

plt.title("Shot Heatmap (All Teams)")
plt.show()