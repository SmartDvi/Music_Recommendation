
import dash_mantine_components as dmc
from dash import *

from utils import df


dropdown = dmc.Select(
                id='dropdown_danceability_level',
                label='Select danceabile Music Level',
                data=[{'label': danceability_level, 'value': danceability_level} for danceability_level in df['danceability_level'].dropna().unique()],
                value=df['danceability_level'].dropna().iloc[0],
                clearable=True,
                style={'marginBottom': "20px"}
        )

track_genre_drp = dmc.Select(
            id='dropdown_track_genre',
            label='Select track_genre Music',
            data=[{'label': track_genre, 'value': track_genre} for track_genre in df['track_genre'].dropna().unique()],
            value=df['track_genre'].dropna().iloc[0],
            clearable=True,
            style={'marginBottom': "20px"}
        )



p_dropdown = dmc.Select(
                id='dropdown_danceability_level',
                label='Select danceabile Music Level',
                data=[{'label': danceability_level, 'value': danceability_level} for danceability_level in df['danceability_level'].dropna().unique()],
                value=df['danceability_level'].dropna().iloc[0],
                clearable=True,
                style={'marginBottom': "20px"}
        )


mood_options =dmc.Group( [
    dmc.Checkbox(
        label=mood,  
        value=mood  
    )
    for mood in df['mood_indicator'].unique()
],
justify='center',
grow=True)

# Create the checkbox group
mood_pd = dmc.CheckboxGroup(
    id="check_box",
    label="Check mood to predict",
    withAsterisk=True,
    mb=10,
    children=mood_options,  
    value=["Calm"]  
)



#print("Available columns in df:", df.columns)
#print("Sample rows in df:")
#print(df.head())
#print(df.info())
#print(f"the cplumn: {df['mood_indicator'].value_counts()}")
#print(f"the cplumn: {df['track_name'].value_counts()}")
grouped_data = df.groupby("energy_level")["energy"].sum().reset_index()
print(grouped_data)