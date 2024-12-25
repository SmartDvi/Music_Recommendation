import pandas as pd
import numpy as np
import plotly.express as px



df = pd.read_csv('C:\\Users\\Moritus Peters\\Downloads\\dataset.csv')
#df = pd.read_csv('https://raw.githubusercontent.com/SmartDvi/Music_Recommendation/main/dataset.csv')

# Convert duration to minutes
df['duration_min'] = df['duration_ms'] / 60000

# Categorize loudness_level
df['loudness_level'] = pd.cut(
    df['loudness'], 
    bins=[-100, -40, -20, -10, -5, 0], 
    labels=['Very Quiet', 'Quiet', 'Moderate', 'Loud', 'Very Loud'], 
    include_lowest=True
)

# Categorize energy_level
df['energy_level'] = pd.cut(
    df['energy'], 
    bins=[0, 0.33, 0.66, 1], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Categorize danceability_level
df['danceability_level'] = pd.cut(
    df['danceability'], 
    bins=[0, 0.33, 0.66, 1], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Categorize tempo_category
df['tempo_category'] = pd.cut(
    df['tempo'], 
    bins=[0, 60, 120, 180, 300], 
    labels=['Slow', 'Medium', 'Fast', 'Very Fast'], 
    include_lowest=True
)

# Categorize explicit_flag
df['explicit_flag'] = df['explicit'].replace({True: 'Explicit', False: 'Non-Explicit'})

# Categorize popularity_level
df['popularity_level'] = pd.cut(
    df['popularity'], 
    bins=[0, 50, 75, 100], 
    labels=['Low', 'Medium', 'High'], 
    include_lowest=True
)

# Define mood_indicator using valence and energy
conditions = [
    (df['valence'] > 0.5) & (df['energy'] > 0.5),
    (df['valence'] > 0.5) & (df['energy'] <= 0.5),
    (df['valence'] <= 0.5) & (df['energy'] > 0.5),
    (df['valence'] <= 0.5) & (df['energy'] <= 0.5)
]
choices = ['Happy', 'Calm', 'Energetic', 'Sad']
df['mood_indicator'] = np.select(conditions, choices, default='Unknown')


color_mapping1 = {
    'Low' : 'red',
    'Medium': 'yellow',
    'High' : 'green'
}





def generate_plotly_colors(unique_values, colorscale="Viridis"):
    """
    Generate a color mapping for unique values using Plotly's color scales.

    Parameters:
    - unique_values (list): List of unique values to map colors to.
    - colorscale (str): Name of the Plotly colorscale to use.

    Returns:
    - dict: A dictionary mapping each unique value to a color.
    """
    num_values = len(unique_values)
    color_palette = px.colors.sample_colorscale(colorscale, [i / (num_values - 1) for i in range(num_values)])
    return {value: color for value, color in zip(unique_values, color_palette)}

