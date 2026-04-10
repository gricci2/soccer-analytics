import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import seaborn as sns

passes_df = pd.read_csv("../../data/processed/pass_locations_all.csv")

passes_df = passes_df.dropna(subset=['x', 'y'])

passes_df = passes_df.sample(n=200000, random_state=42)

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

sns.kdeplot(
    x=passes_df['x'],
    y=passes_df['y'],
    fill=True,
    cmap='Reds',
    alpha=0.6,
    thresh=0.05,
    ax=ax
)

plt.title("Pass Heatmap (All Teams)")
plt.show()