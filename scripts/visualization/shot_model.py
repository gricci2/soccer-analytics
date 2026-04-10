import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from scipy.ndimage import gaussian_filter

shots_df = pd.read_csv("../../data/processed/shot_model.csv")

shots_df = shots_df.dropna(subset=['x', 'y'])

shots_df['distance_to_goal'] = np.sqrt((120 - shots_df['x'])**2 + (40 - shots_df['y'])**2)

# goal posts at y = 36.34 and y = 43.66 (scaled to pitch 0-80)
goal_top = 36.34
goal_bottom = 43.66
goal_x = 120

# compute angles in radians
shots_df['angle_to_goal'] = np.arctan2(goal_top - shots_df['y'], goal_x - shots_df['x']) - \
                            np.arctan2(goal_bottom - shots_df['y'], goal_x - shots_df['x'])

# take absolute value (just in case)
shots_df['angle_to_goal'] = np.abs(shots_df['angle_to_goal'])

X = shots_df[['x', 'y', 'distance_to_goal', 'angle_to_goal']]
y = shots_df['goal']

#split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#create model
model = LogisticRegression(max_iter=1000)

#train model
model.fit(X_train, y_train)

#use model on unseen data (predict)
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

#see accurate the model is
print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_prob))


roc_xgb = roc_auc_score(shots_df['goal'], shots_df['shot_statsbomb_xg'])
print("StatsBomb xG ROC AUC:", roc_xgb)

print(model.coef_)
print(model.intercept_)

#create predicted xG heatmap

# create x and y ranges
x_range = np.arange(0, 121, 1)
y_range = np.arange(0, 81, 1)

# create meshgrid
xx, yy = np.meshgrid(x_range, y_range)

# distance to goal
distance_to_goal = np.sqrt((120 - xx)**2 + (40 - yy)**2)

# angle to goal
goal_top = 36.34
goal_bottom = 43.66
angle_to_goal = np.abs(np.arctan2(goal_top - yy, 120 - xx) - np.arctan2(goal_bottom - yy, 120 - xx))

# flatten the arrays to make a DataFrame
grid_df = pd.DataFrame({
    'x': xx.ravel(),
    'y': yy.ravel(),
    'distance_to_goal': distance_to_goal.ravel(),
    'angle_to_goal': angle_to_goal.ravel()
})

# predict probabilities
xg_probs = model.predict_proba(grid_df)[:, 1]

# reshape back to grid for heatmap
xg_grid = xg_probs.reshape(xx.shape)

# create pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(10, 7))

xg_grid_smooth = gaussian_filter(xg_grid, sigma=0)

# plot heatmap with imshow
pcm = ax.imshow(
    xg_grid_smooth, 
    origin='lower',            
    extent=[0, 120, 0, 80],    
    cmap='Reds',
    alpha=0.4,
    aspect='auto'
)

# pixel centers
x_edges = np.linspace(0, 120, xg_grid.shape[1]+1)
y_edges = np.linspace(0, 80, xg_grid.shape[0]+1)
x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2

# create 2D grid of centers
xx_centers, yy_centers = np.meshgrid(x_centers, y_centers)
# loop over every square in the grid
threshold = 0.02  
for i in range(xx.shape[0]):
    for j in range(xx.shape[1]):
        if xg_grid[i, j] > threshold:
            ax.text(
                xx_centers[i, j],
                yy_centers[i, j],
                f"{xg_grid[i, j]:.2f}",  
                color='black', 
                fontsize=5,              
                ha='center', 
                va='center',
                clip_on=True
            )

# add colorbar
cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label('Predicted xG')

plt.title("Predicted xG Heatmap (Logistic Regression: location, distance, angle)")
plt.show()