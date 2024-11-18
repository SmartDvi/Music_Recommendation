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
p_dropdown = dmc.Select(
            id='dropdown_popularity_level',
            label='Select danceabile Music Level',
            data=[{'label': popularity_level, 'value': popularity_level} for popularity_level in df['popularity_level'].dropna().unique()],
            value=df['popularity_level'].dropna().iloc[0],
            clearable=True,
            style={'marginBottom': "20px"}
        )
mode_indicator = html.Div(
    [
        dmc.Checkbox(
            id=f'mood_indicator_{i}',
            label=row,
            checked=False,  # Set default checked status if required
            style={"marginTop": '5px', "marginLeft": '33px'}
        )
        for i, row in enumerate(df['mood_indicator'].dropna().unique())
    ]
)


#print("Available columns in df:", df.columns)
#print("Sample rows in df:")
#print(df.head())
#print(df.info())
#print(f"the cplumn: {df['mood_indicator'].value_counts()}")
#print(f"the cplumn: {df['track_name'].value_counts()}")
grouped_data = df.groupby("energy_level")["energy"].sum().reset_index()
print(grouped_data)