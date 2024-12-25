import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import pandas as pd
from dash import *
from utils import df, generate_plotly_colors
from components import dropdown, p_dropdown, track_genre_drp, mood_options

register_page(__name__, path="/insights", name="Insight Dashboard", order=2)

# Mood Colors
COLOR_MAP = {
    'Happy': 'green',
    'Energetic': 'yellow',
    'Sad': 'orange',
    'Unhealthy': 'red',
    'Calm': 'purple',
}


# Helper Function: Artist Mood Popularity
def artist_mood_popularity(mood_indicator, track_genre):
    filtered_df = df[(df['mood_indicator'] == mood_indicator) & (df['track_genre'] == track_genre)]
    if filtered_df.empty:
        return dmc.Text("No data available for the selected mood and genre.", c="dimmed", ta="center")

    data = filtered_df.groupby('artists')['popularity'].sum().reset_index()
    top_20 = data.nlargest(20, 'popularity')
    least_20 = data.nsmallest(20, 'popularity')
    combined = pd.concat([top_20, least_20])

    return dmc.BarChart(
        id=f'pop_tab_{mood_indicator}',
        datakey='artists',
        data=combined.to_dict('records'),
        orientation='vertical',
        yAxisProps={"width": 80},
        series=[
            {
                "name": "Popularity",
                "data": combined['popularity'].tolist(),
                "color": COLOR_MAP.get(mood_indicator, 'blue'),
            }
        ],
    )


# Helper Function: Tabs for Moods
def create_mood_tabs(track_genre):
    return dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.TabsTab('Happy', value='Happy'),
                    dmc.TabsTab('Energetic', value='Energetic'),
                    dmc.TabsTab('Sad', value='Sad'),
                    dmc.TabsTab('Calm', value='Calm'),
                ]
            ),
            dmc.TabsPanel(artist_mood_popularity('Happy', track_genre), value='Happy'),
            dmc.TabsPanel(artist_mood_popularity('Energetic', track_genre), value='Energetic'),
            dmc.TabsPanel(artist_mood_popularity('Sad', track_genre), value='Sad'),
            dmc.TabsPanel(artist_mood_popularity('Calm', track_genre), value='Calm'),

        ],
        value='Happy',
        id='return_tabs',
    )


# Metric Card Helper Function
def create_metric_card(title, value, color):
    return dmc.Card(
        dmc.Group(
            [
                dmc.Text(title, size="sm", c="dimmed"),
                dmc.Text(value, size="xl", c=color, fw=700),
            ],
            justify="center",
        ),
        withBorder=True,
        shadow="sm",
        radius="md",
        p="lg",
        style={"background": "#f5f5f5"},
    )


# Layout
layout = dmc.MantineProvider(
    [
        # Header Section
        dmc.Container(
            dmc.Text(
                "Insight Dashboard",
                tt="uppercase",
                size="xl",
                c="indigo",
                ta="center",
                td="underline",
                fw=700,
                py=20,
            ),
            fluid=True,
        ),



        # Key Insight Section
        dmc.Container(
            dmc.Grid(
                [
                    dmc.GridCol(create_metric_card("Total Tracks", "1,300", "blue"), span=3),
                    dmc.GridCol(create_metric_card("Average Popularity", "68%", "green"), span=3),
                    dmc.GridCol(create_metric_card("Top Genre", "Acoustic", "purple"), span=3),
                    dmc.GridCol(create_metric_card("Average Duration (min)", "3.5", "teal"), span=3),
                ],
                gutter="xl",
            ),
            fluid=True,
            py=20,
        ),

        # Filters Section
        dmc.Grid(
            [
                dmc.GridCol(dropdown, span=3),
                dmc.GridCol(p_dropdown,  span=3),
                dmc.GridCol(track_genre_drp, span=3),
            ],
            gutter="xl",
            justify='center'
        ),

        # Main Data and Insights Section
        dmc.Container(
            dmc.Grid(
                [
                    # Left Section: Popularity Graph
                    dmc.GridCol(
                        dmc.Paper(
                            [
                                dmc.Text(
                                    "Artist Popularity by Mood",
                                    size="md",
                                    fw=600,
                                    ta="center",
                                    mt="10",
                                ),
                                dmc.Container(
                                    id="artist_popularity",
                                    style={"height": "620px"}
                                ),
                            ],
                            p="sm",
                            shadow="sm",
                            radius="md",
                            withBorder=True,
                        ),
                        span=3,
                    ),

                    # Right Section: Nested Grids for Various Insights
                    dmc.GridCol(
                        [
                            # First Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Average Popularity by Mood", size="sm", fw=600, mb=10),
                                                dcc.Graph(
                                                    id="Average_Popularity_Mood",
                                                    style={"height": "255px"},
                                                    config={"displayModeBar": True, "responsive": True},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=5,
                                    ),
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Popularity vs Danceability by Genre", size="sm", ta="center", fw=600, mb=10),
                                                dcc.Graph(
                                                    id="duration_vs_danceability",
                                                    style={"height": "255px"},
                                                    config={"displayModeBar": True, "responsive": True},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=7,
                                    ),
                                ],
                                gutter="sm",
                            ),

                            dmc.Grid(
                                dmc.GridCol(mood_options)
                                
                            ),

                            # Second Row of Right Section
                            dmc.Grid(
                                [
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Genre Distribution", size="sm", fw=600, mb=10),
                                                dmc.Container(
                                                    id="genre_distribution",
                                                    style={"height": "250px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=6,
                                    ),
                                    dmc.GridCol(
                                        dmc.Paper(
                                            [
                                                dmc.Text("Mood Analysis", size="sm", fw=600, mb=10),
                                                dmc.Container(
                                                    id="mood_analysis",
                                                    style={"height": "250px"},
                                                ),
                                            ],
                                            p="md",
                                            shadow="md",
                                            withBorder=True,
                                        ),
                                        span=6,
                                    ),
                                ],
                                gutter="sm",
                            ),
                        ],
                        span=9,
                    ),
                ],
                gutter="sm",
            ),
            fluid=True,
            py=15,
        ),
    ],
)


# Callbacks
@callback(
    Output("duration_vs_danceability", "figure"),
    Input("dropdown_danceability_level", "value"),
)
def pop_dan(selected_dan_level):
    # Filter the dataframe based on the selected danceability level
    filtered_df = df if not selected_dan_level else df[df['danceability_level'] == selected_dan_level]

    # List of relevant genres you want to keep
    relevant_genres = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'blues', 
                       'classical', 'dance', 'disco', 'electronic', 'indie', 'jazz', 'metal', 'pop', 
                       'rock', 'soul', 'techno', 'trance']
    
    # Filter the dataframe to only include rows where track_genre is in the relevant genres list
    filtered_df = filtered_df[filtered_df['track_genre'].isin(relevant_genres)]
    
    # Create the scatter plot
    fig = px.scatter(
        filtered_df,
        x="danceability",
        y="popularity",
        color="track_genre",
        size="energy",
        hover_data=["track_name", "artists"],
        labels={"danceability": "Danceability", "popularity": "Popularity"},
    )
    
    # Update layout to remove margins
    fig.update_layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
    
    return fig



@callback(
    Output("artist_popularity", "children"),
    Input("dropdown_track_genre", "value"),
)
def update_tabs(selected_track_genre):
    if not selected_track_genre:
        raise PreventUpdate
    return create_mood_tabs(selected_track_genre)


