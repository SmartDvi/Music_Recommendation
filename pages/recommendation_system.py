import dash
from dash import *
import dash_ag_grid as dag
import dash_mantine_components as dmc
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np

register_page(__name__, path='/recommendation_system', title='recommendation_system')


from utils import df

# Drop rows with null values in important columns
df = df.dropna(subset=['artists', 'album_name', 'track_name'])

# Select features and scale them
features = ['danceability', 'energy', 'valence', 'acousticness', 'tempo']
df_features = df[features]
scaler = StandardScaler()
df_features_scaled = scaler.fit_transform(df_features)

# Fit a Nearest Neighbors model
nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(df_features_scaled)

# Define the layout of the app
layout = dmc.MantineProvider(
    defaultColorScheme='green',
    children=[
       
                dmc.Grid(
                    children=[
                        dmc.GridCol(
                            [
                                dmc.Text('Spotify Music Recommendation'),
                                dmc.Textarea(
                                    id='input_area',
                                    label='Select a Music ',
                                    placeholder='Enter genre, mood, energy level, artist, track name, etc.',
                                
                                    autosize=True,
                                    minRows=2
                                ),
                                html.Div(id='carousel-container'),
                            ]
                        )
                    ]
                ),
            dmc.Grid(
                    children=[
                        dmc.GridCol(
                            dag.AgGrid(
                                id='recommendation-table',
                               # style={'height': '400px', 'width': '100%'},
                                columnDefs=[
                                    {"headerName": "Track Name", "field": 'track_name'},
                                    {'headerName': 'Artist', 'field': 'artists'},
                                    {'headerName': 'Album', "field": 'album_name'},
                                    {'headerName': 'Popularity', 'field': 'popularity'},
                                    {'headerName': 'Duration (mins)', 'field': 'duration_min'},
                                    {'headerName': 'Mood', 'field': 'mood_indicator'}
                                ],
                                rowData=[],
                                rowModelType='clientSide',
                                defaultColDef={'sortable': True, 'filter': True, 'resizable': True}
                            )
                        ),
                        dmc.GridCol(
                            dag.AgGrid(
                                id='validation_table',
                                style={'height': '200px', 'width': '100%'},
                                columnDefs=[
                                    {'headerName': 'Metric', 'field': 'metric'},
                                    {'headerName': 'Value', 'field': 'value'}
                                ],
                                rowData=[]
                            )
                        )
                    ]
                )
            
        
    ]
)
# developing the callback to update recommendation and validation metrics
@callback(
    [Output('carousel-container', 'children'),
     Output('recommendation-table', 'rowData'),
     Output('validation_table', 'rowData')],
     [Input('input_area', 'value')]
)
def update_recommendations(input_text):
    if not input_text:
        return dash.no_update, dash.no_update, dash.no_update
    
    # filter based on input
    filter_condition = (
        df['track_name'].str.contains(input_text, case=False, na=False) |
        df['artists'].str.contains(input_text, case=False, na=False) |
        df['album_name'].str.contains(input_text, case=False, na=False) |
        df['track_genre'].str.contains(input_text, case=False, na=False) |
        df['mood_indicator'].str.contains(input_text, case=False, na=False) |
        df['energy'].str.contains(input_text, case=False, na=False) 
    )

    filtered_df = df[filter_condition]

    # handling empty filtered dataframe
    if filtered_df.empty:
        return [], [], []
    
    # calculate the mean of the filtered features
    input_vector = filtered_df[features].mean().values.reshape(1, -1)
    input_df_scaled = scaler.transform(input_vector)

    # Getting recommendations from nearest neighbors
    distances, indices = nbrs.kneighbors(input_df_scaled)
    top_recommendations = df.iloc[indices[0]]

    # calculate the validation metrics to check the performance of the model
    rmse = np.sqrt(mean_squared_error(df_features_scaled[indices[0]], input_df_scaled))
    mae = mean_absolute_error(df_features_scaled[indices[0]], input_df_scaled)
    avg_distance = np.mean(distances)

    validation_metrics = [
      {'metric': 'RMSE', 'value' : f"{rmse:.4f}"},
      {'metric': 'MAE', 'value': f"{mae:.4f}"},
      {'metri': 'Average Distance', 'value': f"{avg_distance:.4f}"}
   ]
    
    # developing the carousel for sliding the top recommendations
    carousel_items =[
        dmc.Carousel(
            [
                dmc.CarouselSlide(
                    dmc.Center(
                        [
                            dmc.Text(f'Recommendation {i}'),
                            dmc.Text(f'{row['track_name']} by {row['artists']}'),
                            dmc.Text(f'Alum: {row['album_name']} | Mood: {row['mood_indicator']}')

                        ], ta='center', bg='green', h='40%'
                ))
            ]
        )for i, row in top_recommendations.iterrows()
    ]

    table_data = top_recommendations[['track_name', 'artists', 'album_name', 'popularity', 'duration_mins', 'mood_indicator']].to_dict('record')
    return carousel_items, table_data, validation_metrics



