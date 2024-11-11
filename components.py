import dash_mantine_components as dmc

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


