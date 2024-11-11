import pandas as pd
import numpy as np



df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\dataset.csv')
#df = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Music_Recommendation/main/dataset.csv')

#Convert duration_ms to minutes for better interpretability
df['duration_min'] = df['duration_ms'] / 60000

#Categorize the loudness into levels (e.g., Quiet, Moderate, Loud).
df['loudness_level'] = pd.cut(df['loudness'], bins=[-60, -20, -10, 0], labels=['Quiet', 'Moderate', 'Loud'])

#energy_level: Categorize energy into low, medium, and high levels.
df['energy_level'] = pd.cut(df['energy'], bins=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])

# danceability_level: Create categories for danceability (e.g., Low, Medium, High).
df['danceability_level'] = pd.cut(df['danceability'], bins=[0, 0.33, 0.66, 1], labels=['Low', 'Medium', 'High'])

# tempo_category: Categorize tempo into different musical tempo categories (e.g., Slow, Medium, Fast).
df['tempo_category'] = pd.cut(df['tempo'], bins=[0, 60, 120, 180, 300], labels=['Slow', 'Medium', 'Fast', 'Very Fast'])

# explicit_flag: Convert explicit boolean into a more descriptive text (Explicit, Non-Explicit).
df['explicit_flag'] = df['explicit'].replace({True: 'Explicit', False: 'Non-Explicit'})

# popularity_level: Categorize popularity into levels (e.g., Low, Medium, High).
df['popularity_level'] = pd.cut(df['popularity'], bins=[0, 50, 75, 100], labels=['Low', 'Medium', 'High'])


# mood_indicator: Use valence and energy to create a mood indicator (e.g., Happy, Energetic, Sad, Calm).
conditions = [
    (df['valence'] > 0.5) & (df['energy'] > 0.5),
    (df['valence'] > 0.5) & (df['energy'] <= 0.5),
    (df['valence'] <= 0.5) & (df['energy'] > 0.5),
    (df['valence'] <= 0.5) & (df['energy'] <= 0.5)
]
choices = ['Happy', 'Calm', 'Energetic', 'Sad']

# ensure that the default value is alsoo a string to aviod dta type conflict
df['mood_indicator'] = np.select(conditions, choices, default='Unknown')


# Binary column indicating whether the track genre is acoustic.
df['is_acoustic'] = df['track_genre'].apply(lambda x: 'acoustic' in x.lower())